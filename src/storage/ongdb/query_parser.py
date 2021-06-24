import json

from src.model.query import Query, RelationshipType
from src.utils.string_utils import key_value_str


def parse(query: Query) -> str:
    relationship_tmpl: dict = {
        RelationshipType.NONE: "-[{label}: {name} {filter}]-",
        RelationshipType.OUT: "-[{label}: {name} {filter}]->",
        RelationshipType.IN: "<-[{label}: {name} {filter}]-"
    }
    where = []
    query_body = "MATCH"
    for t in query.traverse:
        if t.traverse_from:
            from_type = t.traverse_from.type
            from_label = t.traverse_from.alias
            from_filters = key_value_str(t.traverse_from.filter)
            if t.traverse_from.where:
                where.append(t.traverse_from.where)
            query_body = f"{query_body} ({from_label}: {from_type} {from_filters})"

        relationship_name = t.through.relation
        relationship_alias = t.through.alias
        direction = t.through.direction
        relationship_filters = key_value_str(t.through.filter)
        query_body = "".join([query_body,
                              relationship_tmpl[direction].format(label=relationship_alias,
                                                                  name=relationship_name,
                                                                  filter=relationship_filters)])
        if t.through.where:
            where.append(t.through.where)

        reach_type = t.reach.type
        reach_label = t.reach.alias
        reach_filters = key_value_str(t.reach.filter)
        query_body = f"{query_body} ({reach_label}: {reach_type} {reach_filters})"
        if t.reach.where:
            where.append(t.reach.where)

    where_clause = " ".join(["WHERE", " AND ".join(where)])
    return_fields = " ".join(["RETURN ", ",".join(query.return_attributes)])
    query_body = f"{query_body} {where_clause} {return_fields}"
    return query_body
