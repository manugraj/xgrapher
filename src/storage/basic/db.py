import abc

from src.model.exe_status import StatusInfo
from src.model.node_data import NodeData, Relation, GraphData
from src.model.query import Query
from src.storage.store import StorageDetail, StoreType


class Database(abc.ABC):

    def __init__(self):
        self.connection_detail = StoreType.provide()
        self.type = StoreType.find_type()
        self._connect()

    @abc.abstractmethod
    def _connect(self):
        pass

    @abc.abstractmethod
    def save(self, data: NodeData) -> StatusInfo:
        pass

    @abc.abstractmethod
    def save_relation(self, relation: Relation) -> StatusInfo:
        pass

    @abc.abstractmethod
    def save_graph(self, data: GraphData) -> StatusInfo:
        pass

    @abc.abstractmethod
    def query(self, data: Query):
        pass

    @abc.abstractmethod
    def query_native(self, query: str):
        pass

    def get_connection_detail(self) -> StorageDetail:
        return self.connection_detail

    def get_type(self) -> StoreType:
        return self.type
