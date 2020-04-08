from setuptools import setup


install_requires = [
    'motor==2.1.0',
    'pymongo==3.10.1'
]


test_require = [
    'pytest==5.3.5',
    'pytest-asyncio==0.10.0',
    'ipython==7.12.0'

]

setup(
    name='meliodas',
    version='1.0.8',
    packages=['meliodas'],
    install_requires=install_requires,
    author='Danilo Vargas',
)
