from typing import Optional, List

from pydantic import BaseModel


class Identifier(BaseModel):
    name: str
    value: str

    def __str__(self) -> str:
        return "=".join([self.name, self.value])


class BaseNode(BaseModel):
    type: str
    attributes: Optional[dict]


class IdentifiableNode(BaseNode):
    type: str
    id_field: str
    attributes: Optional[dict]

    def describe(self) -> str:
        return f"{self.type}({self.attributes[self.id_field]})"


class RelationshipData(BaseNode):
    relative: IdentifiableNode

    def identifier(self, start_node: IdentifiableNode):
        return Identifier(name=RelationshipData.identifier_name(),
                          value="-".join([start_node.describe(), self.type, self.relative.describe()]))

    @staticmethod
    def identifier_name():
        return "rid"


class NodeData(IdentifiableNode):
    relationships: Optional[List[RelationshipData]]


class ASide(BaseModel):
    node: IdentifiableNode


class Relation(BaseNode):
    this_side: ASide
    that_side: ASide

    def identifier(self):
        return Identifier(name=RelationshipData.identifier_name(),
                          value="-".join([self.this_side.node.describe(), self.type, self.that_side.node.describe()]))

    @staticmethod
    def identifier_name():
        return RelationshipData.identifier_name()


class GNode(BaseModel):
    type: str
    id_field: str
    attributes: dict

    def describe(self) -> str:
        return f"{self.type}({self.attributes[self.id_field]})"


class GRelationship(BaseModel):
    type: str
    attributes: Optional[dict]

    def identifier(self, start: GNode, end: GNode):
        return Identifier(name=GRelationship.identifier_name(),
                          value="-".join([start.describe(), self.type, end.describe()]))

    @staticmethod
    def identifier_name():
        return RelationshipData.identifier_name()


class Graph(BaseModel):
    start: Optional[GNode]
    through: GRelationship
    reach: GNode


class GraphData(BaseModel):
    graphs: List[Graph]
