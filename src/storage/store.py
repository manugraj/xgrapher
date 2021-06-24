import json
from dataclasses import dataclass
from enum import Enum

from src.config import SystemConfig, Constants


@dataclass
class StorageDetail:
    url: str
    user: str
    pswd: str
    details: dict


class StoreType(Enum):
    ONGDB = "ONGDB"
    NEO4J = "NEO4J"

    @staticmethod
    def find_type():
        return StoreType.__dict__[SystemConfig.get_vital(Constants.STORE_TYPE)]

    @staticmethod
    def provide() -> StorageDetail:
        info = SystemConfig.get(Constants.STORE_INFO)
        return StorageDetail(url=SystemConfig.get_vital(Constants.STORE_URL),
                             user=SystemConfig.get(Constants.STORE_CREDENTIALS_USER),
                             pswd=SystemConfig.get(Constants.STORE_CREDENTIALS_PSWD),
                             details=json.loads(info) if info else {})
