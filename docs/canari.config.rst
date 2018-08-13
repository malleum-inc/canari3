:mod:`canari.config` - Canari Configuration Files
=================================================

.. module:: canari.config
    :synopsis: Canari configuration files
.. moduleauthor:: Nadeem Douba <ndouba@redcanari.com>
.. sectionauthor:: Nadeem Douba <ndouba@redcanari.com>

.. versionadded:: 3.0

-------------
Every Canari transform is provided with access to the Canari configuration files via the ``config`` parameter in
:meth:`Transform.do_transform`. The Canari configuration object gets its data from the ``canari.conf`` file and any
additional child configuration files specified in the ``canari.local.configs`` option. These files are usually located
in the ``.canari/`` directory in your home directory (i.e ``~/.canari/`` in Mac/Linux or ``%HOMEPATH%\.canari\``
in Windows). Canari configuration files are loaded in the following manner:

1. Canari checks to see whether or not the transform package being loaded is in the global Python site-package
   directory. If it is, the ``canari.conf`` file in the global ``.canari`` directory is loaded. Otherwise, the
   ``canari.conf`` file in the current working directory is used, if present.
2. Once the main configuration file is loaded, Canari will inspect the ``canari.local.configs`` option to determine
   whether there are any additional configuration files to be loaded. Typically this option is populated with a list of
   configuration files belonging to all the transform packages that have been installed (via
   :program:`canari create-profile`) using Canari.
3. Canari will then iterate over each configuration filename entry in ``canari.local.configs`` and load the
   configuration files in the same order as they appear in the configuration file. If a configuration option in one
   configuration file shares the same name and section as one from another, the latest configuration value will be used.

Common use-cases for using the configuration file is to retrieve information such as backend API keys or credentials
that you may use to connect to third-party services. Here's an example of how to use the configuration object in your
transforms::

    class MyTransform(Transform):
        def do_transform(request, response, config):
            db = connect_to_db(config['foo.local.username'], config['foo.local.password'])
            results = db.query('SELECT name FROM users WHERE id=?', request.entity.value)
            for r in results:
                response += Phrase(r)
            return response

In the example above, the ``canari.conf`` file would look like this::

    [canari.local]
    configs = foo.conf

    # ...

The transform package's configuration file, ``foo.conf``, would look like this::

    [foo.local]
    username = bar
    password = baz

.. note::

    As a best practice for remote transforms, only backend architectural details and license keys should be stored in
    the configuration file. Client-side API keys can and should be received from the Maltego transform request
    parameters.

The ``config`` parameter in our :meth:`Transform.do_transform` method is a :class:`CanariConfigParser` object. By
default all transform runners instantiate the configuration object using the :func:`load_config` function with no
parameters and pass the result to the transforms. If however, you wish to load a separate configuration file, manually,
you can use the :func:`load_config` function in the following manner:

.. function:: load_config(config_file=None, recursive_load=True)

    :param str config_file: the absolute path to a custom configuration file.
    :param bool recursive_load: ``True`` if your configuration file has a ``canari.local.configs`` option and you wish
                                to load the additional configuration files specified in that option. ``False``
                                otherwise.

    If ``recursive_load`` is ``True`` but your configuration file does not have a ``canari.local`` section or a
    ``configs`` option specified under that section, it will be quietly ignored.

Once loaded, configuration objects can be queried in the following manner (where ``c`` is the configuration object):

.. csv-table::
    :header: Operation,Meaning

    ``'section.name' in c``, Does the configuration contain the specified section.
    ``'section.name.option' in c``, Does the configuration contain the specified section and option.
    ``c['section.name.option']``, Retrieve the value of the specified option and section.

Configuration objects have two additional features over and above regular configuration objects in Python, automatic
type marshalling, and advanced string interpolation.

Automatic Type Marshalling
--------------------------
One of the biggest advantages in using the :class:`CanariConfigParser` over other configuration parsers in Python is its
ability to automatically marshal options to the appropriate type. For example, say you had the following configuration
file::

    [foo.local]
    username = admin
    threshold = 1000
    timeout = 0.5
    servers = 10.0.0.1, 10.0.0.2
    validator = object://foo.validators/simple

These options would translate to the following when retrieve from your transform::

    >>> config['foo.local.username'] # string
    'admin'
    >>> config['foo.local.threshold'] # integer
    1000
    >>> config['foo.local.timeout'] # float
    0.5
    >>> config['foo.local.servers'] # list of strings
    ['10.0.0.1', '10.0.0.2']
    >>> config['foo.local.validator'] # foo.validators.simple object
    <function foo.local.validator at 0x1337b33f>
    >>>

.. attention::

    Options starting with ``object://`` will return the option as a string in remote transform execution mode.

Option String Interpolation
---------------------------
In addition to automatic type marshalling, :class:`CanariConfigParser` objects support additional string interpolation
features. This allows you to reference other options within your configuration file as well as system environment
variables. For example, querying options from the following configuration file::

    [foo.local]
    bar = %(baz)
    baz = 1
    mypaths = ${PATH}:/custom/path

Would result in the following::

    >>> config['foo.local.bar']
    1
    >>> config['foo.local.mypaths']
    /usr/bin:/bin:/usr/local/bin:/custom/path
    >>>

