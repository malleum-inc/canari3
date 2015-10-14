__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2015, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'CanariMode',
    'set_canari_mode',
    'get_canari_mode',
    'is_local_exec_mode',
    'is_debug_exec_mode',
    'is_dispatch_exec_mode',
    'is_remote_exec_mode',
    'is_plume_exec_mode',
    'is_shell_exec_mode',
    'is_unknown_exec_mode',
    'is_local_debug_exec_mode',
    'is_local_dispatch_exec_mode',
    'is_local_unknown_exec_mode',
    'is_remote_plume_debug_exec_mode',
    'is_remote_plume_dispatch_exec_mode',
    'is_remote_unknown_exec_mode',
    'is_local_shell_debug_exec_mode',
    'get_canari_mode_str'
]


class CanariMode:
    """
    Utility class that provides enumeration variables for Canari operating modes as well as a helper function to convert
    numeric representations of those operating modes into human readable strings. Currently there are two primary
    operating modes, Local and Remote. Each operating mode has three context mode bits:

     - Dispatch: disables debugging and operates in production mode.
     - Debug: enables additional debug messaging.
     - Unknown: disables production and debugging modes - operation is not guaranteed.

    One can also specify which runner is used in Remote mode by adding the Plume and Runner operating modes.
    """

    Local = 0x01
    Remote = 0x02
    Debug = 0x04
    Dispatch = 0x08
    Plume = 0x10
    Shell = 0x40
    Unknown = 0x80
    RemotePlumeDispatch = Remote | Dispatch | Plume
    RemotePlumeDebug = Remote | Debug | Plume
    RemoteUnknown = Remote | Unknown
    LocalDispatch = Local | Dispatch
    LocalDebug = Local | Debug
    LocalUnknown = Local | Unknown
    LocalShellDebug = Local | Shell | Debug

    _str_table = {
        Local: 'Local',
        Remote: 'Remote',
        Debug: 'Debug',
        Dispatch: 'Dispatch',
        Plume: 'Plume',
        Shell: 'Shell',
        Unknown: 'Unknown',
        RemotePlumeDispatch: 'Remote (server:Plume, debug:False)',
        RemotePlumeDebug: 'Remote (server:Plume, debug:True)',
        RemoteUnknown: 'Remote (server:?, debug:?)',
        LocalDispatch: 'Local (runner:Canari, debug:False)',
        LocalDebug: 'Local (runner:Canari, debug:True)',
        LocalUnknown: 'Local (runner=?, debug=?)',
        LocalShellDebug: 'Local (runner=shell, debug=True)'
    }

    @classmethod
    def to_str(cls, mode):
        """
        Converts a numeric operating mode into a human readable string.

        :param mode: the numeric operating mode.
        :return: a human readable string that corresponds to the operating mode.
        """
        return cls._str_table.get(mode, cls.Unknown)


# By default the operating mode is unknown.
canari_mode = CanariMode.Unknown


def set_canari_mode(mode=CanariMode.Unknown):
    """
    Sets the global operating mode for Canari. This is used to alter the behaviour of dangerous classes like the
    CanariConfigParser.

    :param mode: the numeric Canari operating mode (CanariMode.Local, CanariMode.Remote, etc.).
    :return: previous operating mode.
    """
    global canari_mode
    old_mode = canari_mode
    canari_mode = mode
    return old_mode


def get_canari_mode():
    """
    Returns the global Canari numeric operating mode.

    :return: global Canari numeric operating mode.
    """
    return canari_mode


def get_canari_mode_str():
    """
    Returns a human readable string of the global Canari operating mode.

    :return: human readable string of the global Canari operating mode.
    """
    return CanariMode.to_str(get_canari_mode())


def is_local_exec_mode():
    """
    Returns a boolean specifying whether Canari is operating in local mode.

    :return: True if Canari is operating in local mode.
    """
    return get_canari_mode() & CanariMode.Local


def is_remote_exec_mode():
    """
    Returns a boolean specifying whether Canari is operating in remote mode.

    :return: True if Canari is operating in remote mode.
    """
    return get_canari_mode() & CanariMode.Remote


def is_debug_exec_mode():
    """
    Returns a boolean specifying whether Canari is operating in debug mode.

    :return: True if Canari is operating in debug mode.
    """
    return get_canari_mode() & CanariMode.Debug


def is_dispatch_exec_mode():
    """
    Returns a boolean specifying whether Canari is operating in dispatch mode.

    :return: True if Canari is operating in dispatch mode.
    """
    return get_canari_mode() & CanariMode.Dispatch


def is_plume_exec_mode():
    """
    Returns a boolean specifying whether Canari is operating in Plume mode.

    :return: True if Canari is operating in Plume mode.
    """
    return get_canari_mode() & CanariMode.Plume


def is_unknown_exec_mode():
    """
    Returns a boolean specifying whether Canari is operating in an unknown mode.

    :return: True if Canari is operating in an unknown mode.
    """
    return get_canari_mode() & CanariMode.Unknown


def is_remote_plume_dispatch_exec_mode():
    """
    Returns a boolean specifying whether Canari is operating in Plume dispatch mode.

    :return: True if Canari is operating in Plume dispatch mode.
    """
    return is_plume_exec_mode() and is_dispatch_exec_mode()


def is_remote_plume_debug_exec_mode():
    """
    Returns a boolean specifying whether Canari is operating in Plume debug mode.

    :return: True if Canari is operating in Plume debug mode.
    """
    return is_plume_exec_mode() and is_debug_exec_mode()


def is_remote_unknown_exec_mode():
    """
    Returns a boolean specifying whether Canari is operating in remote Runner debug mode.

    :return: True if Canari is operating in remote Runner mode.
    """
    return is_remote_exec_mode() and is_unknown_exec_mode()


def is_local_dispatch_exec_mode():
    """
    Returns a boolean specifying whether Canari is operating in local dispatch mode.

    :return: True if Canari is operating in local dispatch mode.
    """
    return is_local_exec_mode() and is_dispatch_exec_mode()


def is_local_debug_exec_mode():
    """
    Returns a boolean specifying whether Canari is operating in local debug mode.

    :return: True if Canari is operating in local debug mode.
    """
    return is_local_exec_mode() and is_debug_exec_mode()


def is_local_unknown_exec_mode():
    """
    Returns a boolean specifying whether Canari is operating in local unknown mode.

    :return: True if Canari is operating in local unknown mode.
    """
    return is_local_exec_mode() and is_unknown_exec_mode()


def is_shell_exec_mode():
    return get_canari_mode() & CanariMode.Shell


def is_local_shell_debug_exec_mode():
    return is_local_exec_mode() and is_shell_exec_mode() and is_debug_exec_mode()