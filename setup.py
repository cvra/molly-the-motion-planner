#! /usr/bin/python

from setuptools import setup

args = dict(
        name='molly',
        version='0.1',
        description='simple path planner',
        packages=['molly'],
        install_requires=['heapdict'],
        author='Pius von Daeniken'
        url='https://github.com/cvra/molly-the-motion-planner'
)

setup(**args)
