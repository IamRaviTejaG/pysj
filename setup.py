#!/usr/bin/env python
"""
Setup script for SplitJoin (PySJ).
"""

from setuptools import setup, find_packages

setup(name='PySJ',
      version='0.0.1',
      description='A command line file splitter & joiner!',
      author='Ravi Teja Gannavarapu',
      author_email='iamravitejag@gmail.com',
      url='https://github.com/ImRaviTejaG/pysj-file-splitter-joiner',
      py_modules=['main'],
      python_requires='>=3',
      install_requires=['click'],
      packages=find_packages(),
      package_dir={'pysj': 'pysj'},
      entry_points='''
            [console_scripts]
            pysj=main:sj
        '''
      )
