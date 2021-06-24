from enum import Enum

from pydantic import BaseModel
from typing import List, Optional, Any


class Status(Enum):
    STARTED = 'STARTED'
    RUNNING = 'RUNNING'
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'
    COMPLETED_WITH_WARN = 'COMPLETED WITH WARNINGS'
    COMPLETED_WITH_FAILURES = 'COMPLETED WITH FAILURES'


class AdditionalInfo(BaseModel):
    messages: Optional[List[str]]
    warnings: Optional[List[str]]
    errors: Optional[List[str]]


class StatusInfo(BaseModel):
    process: Status
    info: Optional[AdditionalInfo]


class ExecutionStatus(BaseModel):
    api: str
    status: StatusInfo
    data: Optional[Any]
