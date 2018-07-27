#!/usr/bin/env python

import os
import sys

from setuptools import setup, find_packages


long_description = """
Canari Framework 3
==================

|Build Status| |Doc Status|

Welcome to the Canari 3 repository - the next generation Maltego rapid
transform development framework which allows you to rapidly prototype,
package, and distribute Maltego local and remote transforms. Please
visit the `documentation <http://canari3.readthedocs.io/en/latest/>`__
site for a quick how-to and more in-depth information on the framework
itself.

Sneak Peek
----------

The following is an example of how easy it is to write a quick Maltego
transform in Canari 3:

.. code:: python


    from canari.maltego.entities import Phrase, Person

    class HelloWorld(Transform):
        \"\"\"This transform says hello to a person entity.\"\"\"

        # The transform input entity type.
        input_type = Person

        def do_transform(self, request, response, config):
            return response + Phrase("Hello " + request.entity.value)

Canari Docker
-------------

You can now dockerize your remote transform packages using
``canari dockerize-package``. This will create a Docker container that
runs Canari Plume fully configured with your remote transforms. You can
easily distribute this container to your Docker swarm. Check out the
documentation on Docker `website <http://docker.com>`__ for more
information on how containers work.

Bug Reports & Questions
-----------------------

Please use the issues page to log any bugs or questions regarding the
Canari Framework.

Kudos
-----

Kudos to our user community for making this release happen. A special
thanks to those of you who have supported the development of Canari 3 by
donating money at our crowd-funding pages. If you like this project,
please consider donating money to help accelerate development.

.. |Build Status| image:: https://circleci.com/gh/redcanari/canari3.svg?style=shield&circle-token=da787a222c75b0a739152d0aa92a9465f702bae6
.. |Doc Status| image:: https://readthedocs.org/projects/canari3/badge/?version=latest


"""

if os.path.exists('README.rst'):
    long_description = open('README.rst').read()

# scripts = [
#     'canari',
#     'dispatcher'
# ]

extras = [
    'readline'
]

requires = [
    'mr.bob',
    'flask',
    'Twisted',
    'pyopenssl',
    'service_identity',
    'pyasn1',
    'boto3',
    'safedexml',
    'lxml',
    'six',
    'future',
    'click',
    'colorama',
    'stringcase'
]

if sys.platform == 'win32':
    requires.append('pyreadline')
    # scripts.extend(['%s.bat' % s for s in scripts])
# else:
#     scripts.append('pysudo')

sys.path.insert(0, 'src')
import canari

setup(
    name='canari',
    author='Nadeem Douba',
    version=canari.version,
    author_email='ndouba@redcanari.com',
    description='Canari Framework - Maltego rapid transform development and execution framework.',
    long_description=long_description,
    license='GPLv3',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    dependency_links=[],
    url='https://github.com/redcanari/canari',
    # scripts=[os.path.join('scripts', s) for s in scripts],
    entry_points='''
    [console_scripts]
    canari=canari.entrypoints:main
    dispatcher=canari.entrypoints:dispatcher
    pysudo=canari.entrypoints:pysudo
    ''',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Framework :: Twisted',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Other Audience',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Server'
    ]
)
