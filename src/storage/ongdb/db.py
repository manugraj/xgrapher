import json
from dataclasses import dataclass
from py2neo import Graph, Node, Relationship
from typing import List

from src.exception import IdNotFound, NoStartNodeFound
from src.model.exe_status import StatusInfo, Status, AdditionalInfo
from src.model.node_data import NodeData, RelationshipData, Identifier, Relation, IdentifiableNode, GraphData, GNode, \
    GRelationship
from src.model.query import Query
from src.storage.basic.db import Database
from src.storage.ongdb import query_parser

ID_FIELD = 'id_field'


@dataclass
class Relative:
    end_node: Node
    end_node_type: str
    end_node_identifier: str
    relationship: Relationship
    relationship_type: str
    relationship_identifier: str


class ONgDB(Database):

    def query_native(self, query: str):
        response = self.graph().run(query).data()
        return {'response': response}

    def save_relation(self, relation: Relation) -> StatusInfo:
        txn = self.graph().begin()
        try:
            this_side = relation.this_side
            that_side = relation.that_side
            start_node = ONgDB._node(this_side.node)
            end_node = ONgDB._node(that_side.node)
            relationship = ONgDB._relation(start_node, relation, end_node)
            txn.merge(start_node, this_side.node.type, this_side.node.id_field)
            txn.merge(end_node, that_side.node.type, that_side.node.id_field)
            txn.merge(relationship, relation.type, relation.identifier_name())
            txn.commit()
            return StatusInfo(process=Status.SUCCESS)
        except Exception as e:
            txn.rollback()
            return StatusInfo(process=Status.FAILURE, info=AdditionalInfo(errors=[str(e)]))

    def _connect(self):
        self.graph = lambda: Graph(self.connection_detail.url)

    def save(self, node_data: NodeData) -> StatusInfo:
        txn = self.graph().begin()
        try:
            start_node = ONgDB._node(node_data)
            txn.merge(start_node, node_data.type, node_data.id_field)
            merge_able = ONgDB._resolve_relatives(node_data, start_node)
            for each in merge_able:
                txn.merge(each.end_node, each.end_node_type, each.end_node_identifier)
                txn.merge(each.relationship, each.relationship_type, each.relationship_identifier)
            txn.commit()
            return StatusInfo(process=Status.SUCCESS)
        except Exception as e:
            txn.rollback()
            return StatusInfo(process=Status.FAILURE, info=AdditionalInfo(errors=[str(e)]))

    @staticmethod
    def _resolve_relatives(data: NodeData, start_node: Node) -> List[Relative]:
        merge_able = []
        if data.relationships:
            for relationship in data.relationships:
                end_node = ONgDB._node(relationship.relative)
                merge_able.append(Relative(end_node=end_node,
                                           end_node_type=relationship.relative.type,
                                           end_node_identifier=relationship.relative.id_field,
                                           relationship=ONgDB._relationship(data, start_node, relationship, end_node),
                                           relationship_type=relationship.type,
                                           relationship_identifier=relationship.identifier_name()))
        return merge_able

    @staticmethod
    def _node(data: IdentifiableNode):
        attribute_data = data.attributes or {}
        if attribute_data.get(data.id_field, None) is None:
            raise IdNotFound("Id field should be populated in attribute section")
        attribute_data[ID_FIELD] = data.id_field
        node = Node(data.type, **attribute_data)
        node.__primarykey__ = data.id_field
        return node

    @staticmethod
    def _relationship(start_node_data: NodeData, start_node, relationship: RelationshipData, end_node):
        attribute_data = relationship.attributes or {}
        identifier = relationship.identifier(start_node=start_node_data)
        attribute_data[identifier.name] = identifier.value
        attribute_data[ID_FIELD] = identifier.name
        return Relationship(start_node, relationship.type, end_node, **attribute_data)

    @staticmethod
    def _relation(start_node, relation: Relation, end_node):
        attribute_data = relation.attributes or {}
        identifier = relation.identifier()
        attribute_data[identifier.name] = identifier.value
        attribute_data[ID_FIELD] = identifier.name
        return Relationship(start_node, relation.type, end_node, **attribute_data)

    def query(self, data: Query):
        return self.query_native(query_parser.parse(data))

    def save_graph(self, node_data: GraphData) -> StatusInfo:
        current_start_node = None
        current_start_gnode = None
        txn = self.graph().begin()
        try:
            for graph in node_data.graphs:
                if graph.start:
                    current_start_gnode = graph.start
                    current_start_node = ONgDB._gnode(current_start_gnode)
                    txn.merge(current_start_node, current_start_gnode.type, current_start_gnode.id_field)
                if current_start_node is None or current_start_node is None:
                    raise NoStartNodeFound("No start node found")

                if graph.through and graph.reach:
                    reached_gnode = graph.reach
                    reached_node = ONgDB._gnode(reached_gnode)
                    relationship = ONgDB._grelationship(current_start_gnode, current_start_node,
                                                        graph.through,
                                                        reached_node,
                                                        reached_gnode)
                    txn.merge(reached_node, reached_gnode.type, reached_gnode.id_field)
                    txn.merge(relationship, graph.through.type, GRelationship.identifier_name())
                    current_start_node = reached_node
                    current_start_gnode = reached_gnode
            txn.commit()
            return StatusInfo(process=Status.SUCCESS)
        except Exception as e:
            txn.rollback()
            return StatusInfo(process=Status.FAILURE, info=AdditionalInfo(errors=[str(e)]))

    @staticmethod
    def _gnode(gnode: GNode):
        attribute_data = gnode.attributes
        if attribute_data.get(gnode.id_field, None) is None:
            raise IdNotFound("Id field should be populated in attribute section")
        attribute_data[ID_FIELD] = gnode.id_field
        node = Node(gnode.type, **attribute_data)
        node.__primarykey__ = gnode.id_field
        return node

    @staticmethod
    def _grelationship(start_gnode: GNode, start_node: Node, grelationship: GRelationship, end_node: Node,
                       end_gnode: GNode):
        attribute_data = grelationship.attributes or {}
        rid: Identifier = grelationship.identifier(start_gnode, end_gnode)
        attribute_data[rid.name] = rid.value
        attribute_data[ID_FIELD] = rid.name
        return Relationship(start_node, grelationship.type, end_node, **attribute_data)
