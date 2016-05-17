# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.MD') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='photo-dedup',
    version='0.1',
    description='A simple photo deduplicator tool written in Python',
    long_description=readme,
    author='Paul Yuan',
    author_email='puyuan1@gmail.com',
    url='https://github.com/puyuan',
    install_requires=[
        'markdown',
    ],
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)