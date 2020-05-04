import asyncio
from datetime import datetime

import pymongo
from pytest import mark

from meliodas.model import Model


class ModelTest(Model):
    _model = 'test'
    sort = [('age', pymongo.ASCENDING)]

    def __init__(self, **kwargs):
        self._id = kwargs.get('id', '')
        self._first_name = kwargs.get('first_name', '')
        self._last_name = kwargs.get('last_name', '')
        self._age = kwargs.get('age', '')
        self._address = kwargs.get('address', '')
        self._created = kwargs.get('created', '')

    @property
    def id(self):
        return self._id

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def age(self):
        return self._age

    @property
    def created(self):
        return self._created


@mark.asyncio
async def test_create_model_success(event_loop):
    test_model = await ModelTest.create(first_name='Danilo', last_name='Vargas', age=25)
    assert test_model.first_name is 'Danilo'
    assert test_model.last_name is 'Vargas'
    assert test_model.age is 25
    created = datetime.fromisoformat(str(test_model.created))
    assert type(created) is datetime
    assert type(test_model) is ModelTest


@mark.asyncio
async def test_create_model_error(event_loop):
    test_model = await ModelTest.create()
    assert test_model.first_name is ''
    assert test_model.last_name is ''
    assert test_model.age is ''
    assert type(test_model) is ModelTest


@mark.asyncio
async def test_filter_model_success(event_loop):
    test_model = await ModelTest.create(first_name='Danilo', last_name='Vargas', age=25, address='Cra 11')
    assert test_model.first_name is 'Danilo'
    assert test_model.last_name is 'Vargas'
    assert test_model.age is 25
    assert type(test_model) is ModelTest
    records = await ModelTest.filter(page=1)
    assert len(records) == 1
    assert records[0]['first_name'] == 'Danilo'
    assert records[0]['last_name'] == 'Vargas'
    assert records[0]['age'] == 25
    assert records[0]['address'] == 'Cra 11'


@mark.asyncio
async def test_get_model_success(event_loop):
    test_model = await ModelTest.create(first_name='Danilo', last_name='Vargas', age=25)
    record = await ModelTest.get_or_none(id=test_model.id)
    assert record.id == test_model.id
    assert record.first_name == 'Danilo'
    assert record.last_name == 'Vargas'
    assert record.age == 25


@mark.asyncio
async def test_get_model_fail(event_loop):
    record = await ModelTest.get_or_none(id='12345')
    assert record is None


@mark.asyncio
async def test_update_model_success(event_loop):
    test_model = await ModelTest.create(first_name='Danilo', last_name='Vargas', age=25)
    record = await ModelTest.update(_id=test_model.id, first_name='Carlos', last_name='Caviedes', age=26)
    record = await ModelTest.get_or_none(id=record.id)
    assert record.id == test_model.id
    assert record.first_name == 'Carlos'
    assert record.last_name == 'Caviedes'
    assert record.age == 26


@mark.asyncio
async def test_search_model_success(event_loop):
    test_model = await ModelTest.create(first_name='Danilo', last_name='Vargas', age=25, address='Cra 12')
    records = await ModelTest.search(age=25)
    assert records[0]['id'] == test_model.id
    assert records[0]['first_name'] == test_model.first_name
    assert records[0]['last_name'] == test_model.last_name
    assert records[0]['age'] == test_model.age
    records = await ModelTest.search(page=1, age=25)
    assert records[0]['id'] == test_model.id
    assert records[0]['first_name'] == test_model.first_name
    assert records[0]['last_name'] == test_model.last_name
    assert records[0]['age'] == test_model.age
    assert records[0]['address'] == 'Cra 12'


@mark.asyncio
async def test_count_model_success(event_loop):
    await ModelTest.create(first_name='Danilo', last_name='Vargas', age=25)
    count = await ModelTest.count()
    assert count == 1


@mark.asyncio
async def test_delete_model_success(event_loop):
    test_model = await ModelTest.create(first_name='Danilo', last_name='Vargas', age=25)
    await ModelTest.delete(_id=test_model.id)
    test_model = await ModelTest.get_or_none(_id=test_model.id)
    assert test_model is None


@mark.asyncio
async def test_last_model_success(event_loop):
    await ModelTest.create(first_name='Danilo', last_name='Vargas', age=25)
    await ModelTest.create(first_name='Tech', last_name='Colombia', age=28)
    await ModelTest.create(first_name='Carlos', last_name='Vargas', age=26)
    model = await ModelTest.last()
    assert model.first_name == 'Carlos'
    assert model.last_name == 'Vargas'
    assert model.age == 26


@mark.asyncio
async def test_last_model_empty_success(event_loop):
    model = await ModelTest.last()
    assert model.first_name == ''
    assert model.last_name == ''
    assert model.age == ''


@mark.asyncio
async def test_ordering_model_success(event_loop):
    await asyncio.gather(
        ModelTest.create(first_name='Danilo', last_name='Vargas', age=25, address='Cra 25'),
        ModelTest.create(first_name='Danilo', last_name='Vargas', age=10, address='Cra 10'),
        ModelTest.create(first_name='Danilo', last_name='Vargas', age=20, address='Cra 20')
    )
    records = await ModelTest.filter(page=1)
    assert records[0]['age'] == 10
    assert records[1]['age'] == 20
    assert records[2]['age'] == 25
