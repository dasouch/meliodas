from pytest import fixture

from meliodas.connection import Connection
from meliodas.settings import DB_NAME


@fixture(autouse=True, scope='function')
async def drop_test_database():
    await Connection().client.drop_database(DB_NAME)
    await Connection().client.drop_database('meliodas')
    yield
