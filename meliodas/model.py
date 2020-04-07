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
    async def _search(cls, page=None,  **kwargs):
        _model = database[cls._model]
        if page:
            return _model.find(kwargs).sort(
                [('created', pymongo.DESCENDING)]).skip(
                (cls.perPage * int(page)) - cls.perPage).limit(cls.perPage)
        return _model.find(kwargs).sort(
            [('created', pymongo.DESCENDING)])

    @classmethod
    async def last(cls):
        _model = database[cls._model]
        records = _model.find({}).sort([('_id', pymongo.DESCENDING)]).limit(1)
        async for record in records:
            return cls(**record)

    @classmethod
    async def count(cls):
        _model = database[cls._model]
        return await _model.count_documents({})

    @classmethod
    async def delete(cls, _id):
        _model = database[cls._model]
        return await _model.delete_one({'id': _id})

    @classmethod
    async def _filter(cls, page):
        _model = database[cls._model]
        return _model.find({}).sort(
            [('created', pymongo.DESCENDING)]).skip(
            (cls.perPage * int(page)) - cls.perPage).limit(cls.perPage)

    @classmethod
    async def filter(cls, page):
        rows = []
        records = await cls._filter(page=page)
        async for record in records:
            rows.append(cls(**record).to_dict())
        return rows

    @classmethod
    async def search(cls, page=None, **kwargs):
        rows = []
        records = await cls._search(page=page, **kwargs)
        async for record in records:
            rows.append(cls(**record).to_dict())
        return rows

    def to_dict(self):
        data = {}
        for attribute, value in self.__dict__.items():
            if attribute.startswith('_'):
                field = attribute[1:]
                try:
                    value = getattr(self, field)
                    if type(value) == datetime:
                        data[field] = value.isoformat()
                    else:
                        data[field] = value
                except AttributeError:
                    data[attribute[1:]] = value
        return data
