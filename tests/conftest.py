from pytest import fixture

from meliodas import settings


@fixture(autouse=True, scope='session')
def setup_test_database():
    settings.DB_NAME = settings.DB_NAME + '_test'
    yield
