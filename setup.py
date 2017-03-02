#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import find_packages, setup

setup(
    name='gallery',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    install_requires=[
        'pymongo',
        'flask',
        'pyopenssl',
        'wechat-sdk'
    ],
    entry_points={
        'console_scripts': [
            'webserver = gallery.main:main'
        ],
    }
)
