from setuptools import setup

setup(
    name='potnanny-api',
    version='0.2.2',
    packages=['potnanny_api'],
    include_package_data=True,
    description='Part of the PotNanny greenhouse controller application. Contains Flask REST API',
    author='Jeff Leary',
    author_email='potnanny@gmail.com',
    url='https://github.com/jeffleary00/potnanny-core',
    install_requires=[
        'requests',
        'passlib',
        'sqlalchemy',
        'marshmallow',
        'flask',
        'flask-restful',
        'flask-jwt-extended',
        'potnanny-core==0.2.2',
    ],
)
