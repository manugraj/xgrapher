from typing import List

from src.model.exe_status import StatusInfo, Status, AdditionalInfo
from src.model.node_data import NodeData, Relation, GraphData
from src.storage.basic.provider import Store


def save(nodes: List[NodeData]):
    return _run(nodes, lambda node: Store.db().save(node))


def save_graph(data: GraphData):
    return Store.db().save_graph(data)


def save_relation(relations: List[Relation]):
    return _run(relations, lambda relation: Store.db().save_relation(relation))


def _run(data: List, action):
    final_status = StatusInfo(process=Status.STARTED, info=AdditionalInfo(messages=[], warnings=[], errors=[]))
    for each_data in data:
        status: StatusInfo = action(each_data)
        if status.info:
            final_status.info.errors.extend(status.info.errors or [])
            final_status.info.warnings.extend(status.info.warnings or [])
            final_status.info.messages.extend(status.info.messages or [])
    if final_status.info.errors and len(final_status.info.errors) > 0:
        final_status.process = Status.COMPLETED_WITH_FAILURES
    elif final_status.info.warnings and len(final_status.info.warnings) > 0:
        final_status.process = Status.COMPLETED_WITH_WARN
    else:
        final_status.process = Status.SUCCESS
    return final_status
