import pymongo
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from uuid import uuid4

from .settings import DB_NAME, DB_PORT, DB_HOST, DB_USER, DB_PASSWORD

if DB_USER and DB_PASSWORD:
    client = AsyncIOMotorClient(f'mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}')
else:
    client = AsyncIOMotorClient(f'mongodb://{DB_HOST}:{DB_PORT}')
database = client[DB_NAME]


class Model:
    _fields = []
    perPage = 10
    sort = []
    _model = None

    @classmethod
    async def create(cls, **kwargs):
        _model = database[cls._model]
        kwargs['id'] = uuid4().hex
        kwargs['created'] = datetime.today()
        await _model.insert_one(kwargs)
        return cls(**kwargs)

    @classmethod
    async def get_or_none(cls, **data):
        _model = database[cls._model]
        record = await _model.find_one(data)
        if record:
            return cls(**record)
        return None

    @classmethod
    async def update(cls, _id, **kwargs):
        _model = database[cls._model]
        await _model.update_one({'id': _id}, {'$set': kwargs})
        record = await cls.get_or_none(id=_id)
        return record

    @classmethod
    async def filter(cls, page):
        _model = database[cls._model]
        return _model.find({}).sort(
            [('created', pymongo.DESCENDING)]).skip(
            (cls.perPage * int(page)) - cls.perPage).limit(cls.perPage)

    @classmethod
    async def search(cls, page,  **kwargs):
        _model = database[cls._model]
        return _model.find(kwargs).sort(
            [('created', pymongo.DESCENDING)]).skip(
            (cls.perPage * int(page)) - cls.perPage).limit(cls.perPage)

    @classmethod
    async def count(cls):
        _model = database[cls._model]
        return await _model.count_documents({})

    @classmethod
    async def delete(cls, _id):
        _model = database[cls._model]
        return await _model.delete_one({'id': _id})
