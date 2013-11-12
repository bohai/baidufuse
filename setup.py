#!/usr/bin/env python
#coding=utf-8

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'File system based baidu netdisk',
    'author': 'boh.ricky',
    'url': 'http://www.bhgeek.com',
    'download_url': 'https://github.com/bohai/baidufuse',
    'author_email': 'boh.ricky@gmail.com',
    'version': '0.1',
    'install_requrire': ['nose', 'baidupan', 'fuse-python'],
    'packages': ['baidufuse'],
    'package_dir': {'baidufuse': 'src'},
    'scripts': ['bin/baidufuse'],
    'name': 'baidufuse'
}

setup(**config)
