from pytest import fixture

from meliodas.model import client
from meliodas.settings import DB_NAME


@fixture(autouse=True, scope='function')
async def drop_test_database():
    await client.drop_database(DB_NAME)
    await client.drop_database('meliodas')
    yield
