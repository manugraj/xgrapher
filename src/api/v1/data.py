from typing import List

from fastapi import APIRouter
from fastapi.requests import Request

from src.core.data import save, save_relation, save_graph
from src.model.exe_status import ExecutionStatus
from src.model.node_data import NodeData, Relation, GraphData

router = APIRouter(prefix="/api/v1/data")


@router.post(path="/", tags=["Data"], response_model=ExecutionStatus, summary="Add Data")
async def add_bias(data: List[NodeData], request: Request):
    return ExecutionStatus(api=request.url.path, status=save(data))


@router.post(path="/graph", tags=["Data"], response_model=ExecutionStatus, summary="Add Data")
async def add_bias(data: GraphData, request: Request):
    return ExecutionStatus(api=request.url.path, status=save_graph(data))


@router.post(path="/relation", tags=["Data"], response_model=ExecutionStatus, summary="Add Data from Relationship")
async def add_bias(data: List[Relation], request: Request):
    return ExecutionStatus(api=request.url.path, status=save_relation(data))
