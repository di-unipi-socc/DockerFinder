
from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pyfinder',
    version='0.0.1',
    description='Crawler and scanner definition of docker finder project',
    long_description=readme,
    author='Davide neri',
    author_email='davideneri18@gmail.com',
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
