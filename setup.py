from setuptools import setup

setup(
    name='potnanny',
    version='0.2.0',
    packages=['potnanny'],
    include_package_data=True,
    install_requires=[
        'requests',
        'passlib',
        'sqlalchemy',
        'marshmallow',
        'flask',
        'flask-restful',
        'flask-jwt-extended',
        'potnanny-core'
    ],
)
