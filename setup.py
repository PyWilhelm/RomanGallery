#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import find_packages, setup

setup(
    name='gallery',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    install_requires=[
        'pymongo'
    ],
    entry_points={
        'console_scripts': [

        ],
    }
)
