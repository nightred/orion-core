# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='orion_core',
    version='0.1.0',
    description='the orion core engine',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Kris Arnott',
    author_email='karnott@jenovarain.com',
    url='https://github.com/nightred',
    license=license,
    packages=find_packages(exclude=('tests', 'docs', 'sample'))
)
