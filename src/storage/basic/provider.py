from src.storage.basic.db import Database
from src.storage.ongdb.db import ONgDB
from src.storage.store import StoreType


class Store:
    _db_impls = {
        StoreType.ONGDB: ONgDB(),
        StoreType.NEO4J: ONgDB()
    }

    @staticmethod
    def db(store_type: StoreType = None) -> Database:
        return Store._db_impls[store_type] if store_type else Store._db_impls[StoreType.find_type()]

    @staticmethod
    def db_type() -> StoreType:
        return StoreType.find_type()
