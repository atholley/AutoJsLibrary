# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='AngularLibrary',
    version='2017.05',
    description='Robot Framework Angular package',
    long_description=readme,
    install_requires=["ExtendedSelenium2Library", "BuiltIn", "yaml"],
    author='Abu Tholley',
    author_email='abu.tholley@gmail.com',
    url='https://github.com/abutholley/AngularLibrary',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
