from string import Template

from src.model.exe_status import Status
from src.model.query import Query, StoredQuery
from src.storage.basic.provider import Store
from src.storage.redis.cache import StoredQueryCache

stored_query_cache = StoredQueryCache()


def run_query(query: Query):
    try:
        return Status.SUCCESS, Store.db().query(query)
    except Exception as e:
        return Status.FAILURE, str(e)


def run_stored_native_query(name: str, parameters: dict = None):
    try:
        stored_query: StoredQuery = stored_query_cache.get(name)
        return Status.SUCCESS, Store.db(stored_query.native_to) \
            .query_native(Template(stored_query.query).substitute(**parameters))
    except Exception as e:
        return Status.FAILURE, str(e)


def store_native_query(query: StoredQuery):
    try:
        return Status.SUCCESS, stored_query_cache.put(query.name, query)
    except Exception as e:
        return Status.FAILURE, str(e)


def get_native_query(name: str):
    try:
        return Status.SUCCESS, stored_query_cache.get(name)
    except Exception as e:
        return Status.FAILURE, str(e)
