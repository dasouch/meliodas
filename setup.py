from setuptools import setup


install_requires = [
    'motor==3.0.0',
    'pymongo==4.2.0',
    'cryptography==39.0.1'
]


test_require = [
    'ipython==7.26.0',
    'pytest==6.2.4',
    'pytest-asyncio==0.15.1',
    'pytest-cov==2.12.1'
]

setup(
    name='meliodas',
    version='1.1.11',
    packages=['meliodas'],
    install_requires=install_requires,
    author='Danilo Vargas',
)
