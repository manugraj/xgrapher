from fastapi import APIRouter
from fastapi.requests import Request

from src.core.query import run_query, get_native_query, run_stored_native_query, store_native_query
from src.model.exe_status import ExecutionStatus, StatusInfo
from src.model.query import Query, StoredQuery

router = APIRouter(prefix="/api/v1/query")


@router.post(path="/", tags=["Query"], summary="Query data")
async def query_data(query: Query, request: Request):
    status, response = run_query(query)
    return ExecutionStatus(api=request.url.path, status=StatusInfo(process=status), data=response)


@router.put(path="/store", tags=["Stored Query"], summary="Store native query for future execution")
async def store_query(query: StoredQuery, request: Request):
    status, response = store_native_query(query)
    return ExecutionStatus(api=request.url.path, status=StatusInfo(process=status), data=response)


@router.get(path="/store", tags=["Stored Query"], summary="Get stored query")
async def get_store_query(name: str, request: Request):
    status, response = get_native_query(name)
    return ExecutionStatus(api=request.url.path, status=StatusInfo(process=status), data=response)


@router.post(path="/store", tags=["Stored Query"], summary="Run stored query")
async def run_native_query(name: str,  request: Request, params: dict = None):
    status, response = run_stored_native_query(name, params)
    return ExecutionStatus(api=request.url.path, status=StatusInfo(process=status), data=response)
