from setuptools import setup


install_requires = [
    'motor==2.5.0',
    'pymongo==3.12.0'
]


test_require = [
    'ipython==7.26.0',
    'pytest==6.2.4',
    'pytest-asyncio==0.15.1',
    'pytest-cov==2.12.1'
]

setup(
    name='meliodas',
    version='1.1.3',
    packages=['meliodas'],
    install_requires=install_requires,
    author='Danilo Vargas',
)
