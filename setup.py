# coding: utf-8

try:
    import setuptools
    from setuptools import setup, find_packages
except ImportError:
    print("Please install setuptools.")

import os
long_description = 'This package help you to create a control program for measurement instruments. It provides you a dynamic way to control your program via a graphical user interface and realtime graph plotting.'

setup(
    name  = 'kuchinawa',
    version = '0.3',
    description = 'Support for creating a control program for measurement instruments',
    long_description = long_description,
    license = 'MIT',
    author = 'Yuki Arai',
    author_email = 'threemeninaboat3247@gmail.com',
    url = 'https://github.com/threemeninaboat3247/kuchinawa',
    keywords = 'measurement',
    packages = find_packages(),
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        'raipy': ['Icons/*.png']
    },
    install_requires = ['pyqtgraph>=0.10.0','pandas'],
    classifiers = [
      'Programming Language :: Python :: 3',
      'Intended Audience :: Science/Research',
      'License :: OSI Approved :: MIT License'
    ]
)
