import asyncio

from motor.motor_asyncio import AsyncIOMotorClient

from meliodas.settings import DB_USER, DB_PASSWORD, DB_SSL, DB_HOST, DB_PORT, DB_CA_CERTS


class Connection:
    client: str = None
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            if DB_USER and DB_PASSWORD and DB_SSL:
                cls.client = AsyncIOMotorClient(
                    f'mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/?ssl=true&tlsCAFile={DB_CA_CERTS}&retryWrites=false')
            elif DB_USER and DB_PASSWORD:
                cls.client = AsyncIOMotorClient(f'mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}')
            else:
                cls.client = AsyncIOMotorClient(f'mongodb://{DB_HOST}:{DB_PORT}')
            cls.client.get_io_loop = asyncio.get_event_loop
            cls._instance = object.__new__(cls)
        return cls._instance
