#!/usr/bin/env python

import os

from setuptools import setup, find_packages

scripts = [
    'src/scripts/canari',
    'src/scripts/dispatcher',
]

if os.name == 'posix':
    scripts.extend(
        [
            'src/scripts/pysudo'
        ]
    )

extras = [
    'readline'
]

requires = [
    'mr.bob',
    'argparse',
    'flask',
    'Twisted',
    'safedexml',
    'lxml'
]

if os.name == 'nt':
    scripts += ['%s.bat' % s for s in scripts]

setup(
    name='canari',
    author='Nadeem Douba',
    version='3.1.2',
    author_email='ndouba@gmail.com',
    description='Rapid transform development and transform execution framework for Maltego.',
    license='GPLv3',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    scripts=scripts,
    zip_safe=False,
    install_requires=requires,
    dependency_links=[]
)
