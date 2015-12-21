Canari Quick Start
==================

.. moduleauthor:: Nadeem Douba <ndouba@redcanari.com>
.. sectionauthor:: Nadeem Douba <ndouba@redcanari.com>

------------

Welcome to the Canari Framework - the world's most advanced rapid transform development framework for Maltego. In this
quickstart tutorial we'll go over how you can take advantage of Canari's powerful feature set to create your own Maltego
transform package. We'll start by developing a local transform package and then migrate that over to a remote transform
package which you can distributed via the `Paterva TDS <https://cetas.paterva.com/TDS/>`_. Enough jibber jabber and
let's get this show on the road.

Installation
------------
Canari requires the following dependencies to get started:

    #. Python 2.7 or later (prior to Python 3) - `Download <https://www.python.org/downloads/>`_
    #. setuptools - `Download <https://pypi.python.org/pypi/setuptools#downloads>`_
    #. virtualenv - `Download <https://pypi.python.org/pypi/virtualenv#downloads>`_

.. note::

    Canari does not support Python version 3.

Installing Dependencies
^^^^^^^^^^^^^^^^^^^^^^^
**Linux Debian-based**

On Debian-based (Ubuntu, Kali, etc.) systems, all these dependencies can be installed using :program:`apt-get`::

    $ sudo apt-get install python2.7 python-virtualenv python-setuptools

**Linux - Fedora-based**

On Fedora-based (Fedora, RedHat, CentOS, etc.) systems, all these dependencies can be installed using :program:`yum`::

    $ sudo yum groupinstall -y 'development tools'
    $ sudo yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel \
         readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel
    $ sudo easy_install virtualenv

**Mac OS/X**

On Mac OS/X, make sure to install `Xcode <https://itunes.apple.com/ca/app/xcode/id497799835?mt=12>`_ from the App Store,
first. Then install the command-line tools like so::

    $ sudo xcode-select --install
    $ wget https://pypi.python.org/packages/source/s/setuptools/setuptools-18.4.tar.gz
    $ tar -zxvf setuptools-18.4.tar.gz
    $ cd setuptools-18.4 && sudo python setup.py install
    $ sudo easy_install virtualenv

Installing Canari
^^^^^^^^^^^^^^^^^
Once you have all your dependencies installed, you can now install Canari. We recommend creating a virtual environment
to reduce clutter in your default Python site-package directory. Virtual environments can be created easily like so::

    $ virtualenv canari3
    New python executable in canari3/bin/python
    Installing setuptools, pip...done.

This will create a completely separate Python environment in the ``canari3`` directory, which you can use to install
custom Python libraries to without the risk of corrupting your default Python environment. Another advantage to virtual
environments is that they can be easily cleaned up if you no longer need them. To activate your virtual environment, do
the following::

    $ source canari3/bin/activate
    $ which python
    canari3/bin/python

.. attention::

    Virtual environments need to be activated every time you create a new terminal session. Otherwise, you'll be using
    the default Python installation. You can automate this process by adding the ``source`` statement above in your
    ``.profile`` or ``.bashrc`` file.

Once you've activated your virtual environment, it is now time to install Canari::

    $ easy_install canari3

.. note::

    One of the advantages of virtual environments is that you no longer have to use :program:`sudo` to install custom
    Python modules.

Now you're all set to get started developing your first transform package!


Hello World!
------------
Let's start by creating our first transform package. This will include an example "Hello World!" transform for your
convenience. To create a transform package we use the :program:`canari` commander like so::

    $ canari create-package hello
    creating skeleton in hello
    --> Project description: My first transform package

    --> Author name [ndouba]:

    --> Author email: myemail@foo.com

    done!
    $

The ``create-package`` commandlet creates the skeleton for your transform package. It starts off by asking you some
standard information about the package and uses that information to populate authorship information in your transform
code.

.. note::

    The :program:`canari` commander has many other commandlets that you can take advantage of. For a full list of
    commands take a look at the output of :program:`canari list-commands`.

If your transform package was successfully created, you should now see a ``hello`` folder in your working directory::

    $ ls
    hello ...

Let's drop into that directory and run our first transform. As mentioned earlier, each time you create a new transform
package, a "Hello World!" transform gets created for your reference. We'll execute this transform using the
:program:`canari debug-transform` transform runner::

    $ cd hello/src
    $ canari debug-transform hello.transforms.helloworld.HelloWorld Bob
    `- MaltegoTransformResponseMessage:
      `- UIMessages:
      `- Entities:
        `- Entity:  {'Type': 'maltego.Phrase'}
          `- Value: Hello Bob!
          `- Weight: 1
        `- Entity:  {'Type': 'maltego.Phrase'}
          `- Value: This way Mr(s). None!
          `- Weight: 1
        `- Entity:  {'Type': 'maltego.Phrase'}
          `- Value: Hi None!
          `- Weight: 1

You'll probably see the output above - but wait why are we seeing ``None`` in places where we'd expect to see ``Bob``.
This is because the example transform also demonstrates the use of transform fields. Go ahead and open the transform in
your favorite text editor located at ``hello/transforms/helloworld.py`` - you should see the following::

    class HelloWorld(Transform):
        # The transform input entity type.
        input_type = Person # <------------------------------------------------ 1

        def do_transform(self, request, response, config):
            person = request.entity
            response += Phrase('Hello %s!' % person.value)
            response += Phrase('This way Mr(s). %s!' % person.lastname) # <---- 2
            response += Phrase('Hi %s!' % person.firstnames) # <--------------- 3
            return response

In our example, the :class:`HelloWorld` transform expects an input type of :class:`Person` (1). If we look in
:meth:`HelloWorld.do_transform` we see that it references the ``person.lastname`` (2) and ``person.firstnames`` (3)
entity fields. Let's pass these fields to our transform runner::

    $ canari debug-transform hello.transforms.helloworld.HelloWorld Bob "person.lastname=Doe#person.firstnames=Bob"
    `- MaltegoTransformResponseMessage:
      `- UIMessages:
      `- Entities:
        `- Entity:  {'Type': 'maltego.Phrase'}
          `- Value: Hello Bob!
          `- Weight: 1
        `- Entity:  {'Type': 'maltego.Phrase'}
          `- Value: This way Mr(s). Doe!
          `- Weight: 1
        `- Entity:  {'Type': 'maltego.Phrase'}
          `- Value: Hi Bob!
          `- Weight: 1

.. note::

    In this case, the entity field names coincidentally matched the names in our code example above. However, this will
    not always be the case. Take a look at the :mod:`canari.maltego.entities` file for a full set of builtin Maltego
    entity definitions and their fields.
.. _bottom: