import json
from json import JSONEncoder

import pymongo
from datetime import datetime, date
from uuid import uuid4

from .connection import Connection
from .settings import DB_NAME


class DateTimeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()


class Model:
    _fields = []
    perPage = 10
    sort = [('created', pymongo.DESCENDING)]
    _model = None
    database_name = DB_NAME

    def set_database_name(self, name):
        self.database_name = name

    def _get_model(self, db_name):
        self.set_database_name(name=db_name)
        return Connection().client[self.database_name][self._model]

    @classmethod
    async def create(cls, db_name=DB_NAME, **kwargs):
        kwargs['id'] = uuid4().hex
        kwargs['created'] = datetime.today()
        obj = cls(**kwargs)
        await obj.save(db_name=db_name)
        return obj

    async def save(self, db_name):
        await self._get_model(db_name=db_name).insert_one(self._to_dict())

    @classmethod
    async def get_or_none(cls, db_name=DB_NAME, **kwargs):
        obj = cls()
        record = await obj._get_model(db_name=db_name).find_one(kwargs)
        if record:
            return cls(**record)
        return None

    @classmethod
    async def update(cls, _id, db_name=DB_NAME, **kwargs):
        obj = cls()
        _model = obj._get_model(db_name=db_name)
        await _model.update_one({'id': _id}, {'$set': kwargs})

    @classmethod
    async def _search(cls, page=None, db_name=DB_NAME, **kwargs):
        obj = cls()
        _model = obj._get_model(db_name=db_name)
        if page:
            return _model.find(kwargs).sort(cls.sort).skip(
                (cls.perPage * int(page)) - cls.perPage).limit(cls.perPage)
        return _model.find(kwargs).sort(cls.sort)

    @classmethod
    async def last(cls, db_name=DB_NAME):
        obj = cls()
        _model = obj._get_model(db_name=db_name)
        records = _model.find({}).sort([('_id', pymongo.DESCENDING)]).limit(1)
        async for record in records:
            return cls(**record)
        return cls()

    @classmethod
    async def count(cls, db_name=DB_NAME):
        obj = cls()
        _model = obj._get_model(db_name=db_name)
        return await _model.count_documents({})

    @classmethod
    async def delete(cls, _id, db_name=DB_NAME):
        obj = cls()
        _model = obj._get_model(db_name=db_name)
        return await _model.delete_one({'id': _id})

    @classmethod
    async def _filter(cls, page, db_name=DB_NAME):
        obj = cls()
        _model = obj._get_model(db_name=db_name)
        return _model.find({}).sort(cls.sort).skip(
            (cls.perPage * int(page)) - cls.perPage).limit(cls.perPage)

    @classmethod
    async def filter(cls, page, db_name=DB_NAME):
        rows = []
        records = await cls._filter(page=page, db_name=db_name)
        async for record in records:
            rows.append(cls(**record).to_dict())
        return rows

    @classmethod
    async def search(cls, page=None, db_name=DB_NAME, **kwargs):
        rows = []
        records = await cls._search(page=page, db_name=db_name, **kwargs)
        async for record in records:
            rows.append(cls(**record).to_dict())
        return rows

    def _to_dict(self):
        data = {}
        for attribute, value in self.__dict__.items():
            if attribute.startswith('_'):
                field = attribute[1:]
                try:
                    data[field] = getattr(self, field)
                except AttributeError:
                    data[attribute[1:]] = value
        return data

    def to_dict(self):
        return json.loads(json.dumps(self._to_dict(), cls=DateTimeEncoder))
