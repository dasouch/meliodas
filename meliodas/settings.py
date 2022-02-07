import os

DB_NAME = os.environ['DB_NAME']
DB_PORT = os.environ['DB_PORT']
DB_HOST = os.environ['DB_HOST']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_SSL = os.environ.get('DB_SSL')
DB_CA_CERTS = os.environ.get('DB_CA_CERTS')
