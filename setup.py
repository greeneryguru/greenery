from setuptools import setup, find_packages

setup(
    name='potnanny',
    version='0.2.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'passlib',
        'sqlalchemy',
        'marshmallow',
        'flask',
        'flask-restful',
        'flask-jwt-extended',
        'bluepy',
        'miflora',
        'mitemp-bt',
        'vesync-outlet',
    ],
)
