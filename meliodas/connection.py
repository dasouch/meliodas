import asyncio
from threading import Lock

from motor.motor_asyncio import AsyncIOMotorClient

from meliodas.settings import DB_USER, DB_PASSWORD, DB_SSL, DB_HOST, DB_PORT, DB_CA_CERTS


class ConnectionMeta(type):

    _instances = {}

    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Connection(metaclass=ConnectionMeta):
    client: str = None

    def __init__(self) -> None:
        if DB_USER and DB_PASSWORD and DB_SSL:
            self.client = AsyncIOMotorClient(
                f'mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/?ssl=true&ssl_ca_certs={DB_CA_CERTS}&retryWrites=false')
        elif DB_USER and DB_PASSWORD:
            self.client = AsyncIOMotorClient(f'mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}')
        else:
            self.client = AsyncIOMotorClient(f'mongodb://{DB_HOST}:{DB_PORT}')
        self.client.get_io_loop = asyncio.get_event_loop
