from src.exception import StoredQueryAlreadyExists
from src.storage.basic.cache import Cache


class StoredQueryCache(Cache):

    def data_prefix(self) -> str:
        return "stored-query-cache-"

    def put(self, key, value) -> bool:
        if super().exists(key):
            raise StoredQueryAlreadyExists(f"Stored query exists for {key}")
        return super().put(key, value)
