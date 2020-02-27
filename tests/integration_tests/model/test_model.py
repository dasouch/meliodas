from pytest import mark

from meliodas.model import Model


class TestModel(Model):
    _model = 'test'

    def __init__(self, **kwargs):
        self._first_name = kwargs.get('first_name', '')
        self._last_name = kwargs.get('last_name', '')
        self._age = kwargs.get('age', '')

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
