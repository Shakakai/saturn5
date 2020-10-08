#!/usr/bin/env python
import os
from setuptools import setup, find_packages
import saturn5

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    long_description = f.read()


setup(
    name='saturn5',
    author='Todd Cullen',
    version=saturn5.__version__,
    license='LICENSE',
    url='https://github.com/shakakai/saturn5',
    description='A Django Development CLI',
    long_description=long_description,
    packages=find_packages('.'),
    install_requires=[
        'docopt',   # For command line arguments.
        'jsonschema',
        'docker'
    ],
    entry_points={
        'console_scripts': [
            'saturn5 = saturn5.entry_points.run_saturn5:run',
        ]
    },
)