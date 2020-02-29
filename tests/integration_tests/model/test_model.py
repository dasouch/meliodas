from pytest import mark

from meliodas.model import Model


class TestModel(Model):
    _model = 'test'

    def __init__(self, **kwargs):
        self._id = kwargs.get('id', '')
        self._first_name = kwargs.get('first_name', '')
        self._last_name = kwargs.get('last_name', '')
        self._age = kwargs.get('age', '')

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


@mark.asyncio
async def test_create_model_success(event_loop):
    test_model = await TestModel.create(first_name='Danilo', last_name='Vargas', age=25)
    assert test_model.first_name is 'Danilo'
    assert test_model.last_name is 'Vargas'
    assert test_model.age is 25
    assert type(test_model) is TestModel


@mark.asyncio
async def test_create_model_error(event_loop):
    test_model = await TestModel.create()
    assert test_model.first_name is ''
    assert test_model.last_name is ''
    assert test_model.age is ''
    assert type(test_model) is TestModel


@mark.asyncio
async def test_filter_model_success(event_loop):
    test_model = await TestModel.create(first_name='Danilo', last_name='Vargas', age=25)
    assert test_model.first_name is 'Danilo'
    assert test_model.last_name is 'Vargas'
    assert test_model.age is 25
    assert type(test_model) is TestModel
    records = await TestModel.filter(page=1)
    assert len(records) == 1
    assert records[0]['first_name'] == 'Danilo'
    assert records[0]['last_name'] == 'Vargas'
    assert records[0]['age'] == 25


@mark.asyncio
async def test_get_model_success(event_loop):
    test_model = await TestModel.create(first_name='Danilo', last_name='Vargas', age=25)
    record = await TestModel.get_or_none(id=test_model.id)
    assert record.id == test_model.id
    assert record.first_name == 'Danilo'
    assert record.last_name == 'Vargas'
    assert record.age == 25


@mark.asyncio
async def test_get_model_fail(event_loop):
    record = await TestModel.get_or_none(id='12345')
    assert record is None


@mark.asyncio
async def test_update_model_success(event_loop):
    test_model = await TestModel.create(first_name='Danilo', last_name='Vargas', age=25)
    record = await TestModel.update(_id=test_model.id, first_name='Carlos', last_name='Caviedes', age=26)
    record = await TestModel.get_or_none(id=record.id)
    assert record.id == test_model.id
    assert record.first_name == 'Carlos'
    assert record.last_name == 'Caviedes'
    assert record.age == 26


@mark.asyncio
async def test_search_model_success(event_loop):
    test_model = await TestModel.create(first_name='Danilo', last_name='Vargas', age=25)
    records = await TestModel.search(age=25)
    assert records[0]['id'] == test_model.id
    assert records[0]['first_name'] == test_model.first_name
    assert records[0]['last_name'] == test_model.last_name
    assert records[0]['age'] == test_model.age
    records = await TestModel.search(page=1, age=25)
    assert records[0]['id'] == test_model.id
    assert records[0]['first_name'] == test_model.first_name
    assert records[0]['last_name'] == test_model.last_name
    assert records[0]['age'] == test_model.age


@mark.asyncio
async def test_count_model_success(event_loop):
    await TestModel.create(first_name='Danilo', last_name='Vargas', age=25)
    count = await TestModel.count()
    assert count == 1


@mark.asyncio
async def test_delete_model_success(event_loop):
    test_model = await TestModel.create(first_name='Danilo', last_name='Vargas', age=25)
    await TestModel.delete(_id=test_model.id)
    test_model = await TestModel.get_or_none(_id=test_model.id)
    assert test_model is None
