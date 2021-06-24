from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from src.storage.store import StoreType


class RelationshipType(Enum):
    IN = "IN"
    OUT = "OUT"
    NONE = "NONE"


class From(BaseModel):
    type: str
    alias: str
    filter: Optional[dict]
    where: Optional[str]


class Through(BaseModel):
    relation: str
    direction: RelationshipType = Field(default=RelationshipType.NONE)
    alias: str
    filter: Optional[dict]
    where: Optional[str]


class Traverse(BaseModel):
    traverse_from: Optional[From]
    through: Through
    reach: From


class Query(BaseModel):
    traverse: List[Traverse]
    return_attributes: List[str]


class StoredQuery(BaseModel):
    name: str
    native_to: StoreType
    query: str
    parameters: Optional[dict]
