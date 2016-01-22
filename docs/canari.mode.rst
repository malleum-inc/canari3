Execution Modes (``canari.mode``)
*********************************

Canari now supports the concept of execution modes. Execution modes allow transform developers to detect what context a transform is operating in (i.e. local or remote, production or debug, etc.) and alter the behaviour of their transforms accordingly. Execution modes also globally enable or disable high-risk functionality or modules that you would normally allow in local transform mode. Here's an example of how a transform can check if it's running as a local or transform::

    from canari.maltego.entities import Phrase,WebSite
    from canari.mode import is_local_exec_mode

    class MyTransform(Transform):
        input_type = WebSite

        def do_transform(self, request, response, config):
            website = request.entity
            if is_local_exec_mode():
                # TODO: do something locally
                pass
            else:
                # TODO: do something remotely
                pass
            return response

You can also determine which transform runner is invoking the transform or whether it is operating in debug versus
production mode, like so::

    # ...
    def do_transform(self, request, response, config):
        if is_local_debug_exec_mode():
            debug("We're running in debug mode.")

Canari modes can also be checked in the global scope to prevent a transform, entity, sensitive function or variable
from being exposed or defined when operating in a particular mode::

    if is_local_exec_mode():
        @RequireSuperUser
        class MyTransform(Transform):
            # Does risky stuff in local mode
            pass
    else:
        class MyTransform(Transform):
            # Does safer stuff in remote mode
            pass

Canari currently supports the following execution modes:

.. csv-table:: Primitive Modes
    :header: Value,Meaning
    :widths: 20, 80

    :attr:`CanariMode.Local`,Transform is running locally.
    :attr:`CanariMode.Remote`,Transform is running remotely.
    :attr:`CanariMode.Debug`,Transform is running in debugging mode.
    :attr:`CanariMode.Dispatch`,Transform is running in production mode.
    :attr:`CanariMode.Plume`,Transform is running in Plume container.
    :attr:`CanariMode.Shell`,Transform is running from :program:`canari shell`.

.. csv-table:: Production Modes
    :header: Value,Meaning
    :widths: 20, 80

    :attr:`CanariMode.LocalDispatch`,Transform running in local production mode.
    :attr:`CanariMode.RemotePlumeDispatch`,Transform is running in Plume production mode.

.. csv-table:: Debugging Modes
    :header: Value,Meaning
    :widths: 20, 80

    :attr:`CanariMode.LocalDebug`,Transform running local debugging mode.
    :attr:`CanariMode.RemotePlumeDebug`,Transform is running in Plume in debugging mode.
    :attr:`CanariMode.LocalShellDebug`,Transform is running running from :program:`canari shell`.

.. csv-table:: Unknown Modes
    :header: Value,Meaning
    :widths: 20, 80

    :attr:`CanariMode.Unknown`,Canari hasn't been initialized and is operating in an unknown mode.
    :attr:`CanariMode.RemoteUnknown`,Canari hasn't been initialized but is operating in remote mode.
    :attr:`CanariMode.LocalUnknown`,Canari hasn't been initialized but is operating in local mode.

The 5 transform runners that come out of the box with Canari operate in the following modes, by default:

.. csv-table::
    :header: Runner,Mode

    :program:`dispatcher`,:attr:`CanariMode.LocalDispatch`
    :program:`canari run-transform`,:attr:`CanariMode.LocalDispatch`
    :program:`canari debug-transform`,:attr:`CanariMode.LocalDebug`
    :program:`canari shell`,:attr:`CanariMode.LocalShellDebug`
    :program:`plume`,:attr:`CanariMode.RemotePlumeDispatch`

Non-primitive operating modes are or'd bitmasks of the primitive operating modes. For example,
:attr:`CanariMode.LocalDebug` is equivalent to ``CanariMode.Local | CanariMode.Debug``. This makes it possible to
perform a broad (i.e. :func:`is_local_exec_mode`) or narrow (i.e. :func:`is_local_debug_exec_mode`) check on an
operating mode. For example::

    >>> from canari.mode import *
    >>> old_mode = set_canari_mode(CanariMode.LocalDebug)
    >>> is_local_exec_mode()
    True
    >>> is_debug_exec_mode()
    True
    >>> is_local_debug_exec_mode()
    True

The :mod:`canari.mode` module provides the following functions:

.. function:: set_canari_mode(mode)

    :param CanariMode mode: the desired operating mode.
    :returns: the old operating mode.

    Sets the Canari operating mode and returns the old one. The old operating mode can be ignored if you never wish to
    restore the original operating mode.

.. function:: get_canari_mode()

    :returns: current Canari operating mode.

    Gets the current Canari operating mode. If a prior call to :func:`canari_set_mode` has not been made, the default
    operating mode is :attr:`CanariMode.Unknown`.

.. function:: get_canari_mode_str()

    :returns: current Canari operating mode as a user-friendly string.

    Gets the current Canari operating mode as a user-friendly string which can be displayed in logs or debugging
    information. For example::

        >>> print get_canari_mode_str()
        Local (runner=shell, debug=True)

As demonstrated earlier, :mod:`canari.mode` provides convenience functions that can be used to query the current
operating mode. These functions return either ``True`` or ``False`` depending on whether the operating mode being
queried has the appropriate operating mode bits set:

.. csv-table::
    :header: Function,Returns ``True`` For Operating Modes

    :func:`is_local_exec_mode`,:attr:`CanariMode.Local*`
    :func:`is_debug_exec_mode`,:attr:`CanariMode.*Debug*`
    :func:`is_dispatch_exec_mode`,:attr:`CanariMode.*Dispatch*`
    :func:`is_remote_exec_mode`,:attr:`CanariMode.Remote*`
    :func:`is_plume_exec_mode`,:attr:`CanariMode.*Plume*`
    :func:`is_shell_exec_mode`,:attr:`CanariMode.*Shell*`
    :func:`is_unknown_exec_mode`,:attr:`CanariMode.*Unknown*`
    :func:`is_local_debug_exec_mode`,:attr:`CanariMode.Local*Debug*`
    :func:`is_local_dispatch_exec_mode`,:attr:`CanariMode.Local*Dispatch*`
    :func:`is_local_unknown_exec_mode`,:attr:`CanariMode.LocalUnknown`
    :func:`is_remote_plume_debug_exec_mode`,:attr:`CanariMode.RemotePlumeDebug`
    :func:`is_remote_plume_dispatch_exec_mode`,:attr:`CanariMode.RemotePlumeDispatch`
    :func:`is_remote_unknown_exec_mode`,:attr:`CanariMode.RemoteUnknown`
    :func:`is_local_shell_debug_exec_mode`,:attr:`CanariMode.LocalShellDebug`
