
from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pyfinder',
    version='0.0.1',
    description='DockerFinder SDK',
    long_description=readme,
    author='Davide neri',
    author_email='davide.neri@di.unipi.it',
    url='https://github.com/di-unipi-socc/DockerFinder',
    license=license,
    packages=find_packages(exclude=('docs'))
)
