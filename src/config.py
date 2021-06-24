import os

from dotenv import load_dotenv
from loguru import logger

is_env_file = os.getenv("CONFIG_SOURCE", "env_file") == "env_file"


class SystemConfig:
    _loaded: bool = False

    @staticmethod
    def load():
        logger.info("Loading from env file: {}", is_env_file)
        if is_env_file:
            logger.info("Loading from env file: xgrapher.conf")
            from dotenv import find_dotenv
            load_dotenv(find_dotenv(filename='xgrapher.conf', raise_error_if_not_found=True))
        SystemConfig._loaded = True

    @staticmethod
    def get(key: str, default=None):
        if not SystemConfig._loaded and is_env_file:
            SystemConfig.load()
        return os.getenv(key, default)

    @staticmethod
    def get_vital(key: str):
        if not SystemConfig._loaded:
            SystemConfig.load()
        env_val = os.getenv(key)
        if env_val:
            return env_val
        raise Exception(f"Mandatory parameter: {key} not available in env | Env file read: {is_env_file} ")


class Constants:
    STORE_TYPE = "STORE_TYPE"
    STORE_URL = "STORE_URL"
    STORE_CREDENTIALS_USER = "STORE_CREDENTIALS_USER"
    STORE_CREDENTIALS_PSWD = "STORE_CREDENTIALS_PSWD"
    STORE_INFO = "STORE_INFO"
