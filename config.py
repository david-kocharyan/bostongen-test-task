import os
import logging

from typing import Union, Optional
from dotenv import load_dotenv
from enum import Enum

load_dotenv()


class AppEnv(str, Enum):
    DEV = "dev"
    PROD = "prod"


def get_env(env_var: str, default_value: Optional[Union[str, int]] = None) -> Optional[Union[str, int]]:
    try:
        return os.environ.get(env_var, default_value)
    except Exception as e:
        logging.error(f"Something went wrong while trying to get the environment variable: {e}")


APP_HOST = get_env("APP_HOST")
APP_PORT = int(get_env("APP_PORT"))
APP_ENV = get_env("APP_ENV")

POSTGRES_DB = get_env("POSTGRES_DB")
POSTGRES_USER = get_env("POSTGRES_USER")
POSTGRES_PASSWORD = get_env("POSTGRES_PASSWORD")
POSTGRES_HOST = get_env("POSTGRES_HOST")

REDIS_HOST = get_env("REDIS_HOST")
