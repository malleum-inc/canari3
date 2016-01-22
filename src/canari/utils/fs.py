import os
import sys

from tempfile import NamedTemporaryFile, gettempdir
from time import time


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2015, Canari Project'
__credits__ = ['Andrew Udvare']

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'flock',
    'FileSemaphore',
    'FileMutex',
    'UniqueFile',
    'CookieFile',
    'PushDir'
]


if os.name == 'nt':
    import msvcrt
    from ctypes import *
    from ctypes.wintypes import BOOL, DWORD, HANDLE

    LOCK_SH = 0x0  # the default
    LOCK_NB = 0x1  # LOCKFILE_FAIL_IMMEDIATELY
    LOCK_EX = 0x2  # LOCKFILE_EXCLUSIVE_LOCK
    LOCK_UN = 0x4  # Unlock file. Not in NT API, just needs to be there.

    # --- the code is taken from pyserial project ---
    #
    # detect size of ULONG_PTR
    def is_64bit():
        return sizeof(c_ulong) != sizeof(c_void_p)


    if is_64bit():
        ULONG_PTR = c_int64
    else:
        ULONG_PTR = c_ulong
    PVOID = c_void_p

    # --- Union inside Structure by stackoverflow:3480240 ---
    class _OFFSET(Structure):
        _fields_ = [
            ('Offset', DWORD),
            ('OffsetHigh', DWORD)]


    class _OFFSET_UNION(Union):
        _anonymous_ = ['_offset']
        _fields_ = [
            ('_offset', _OFFSET),
            ('Pointer', PVOID)]


    class OVERLAPPED(Structure):
        _anonymous_ = ['_offset_union']
        _fields_ = [
            ('Internal', ULONG_PTR),
            ('InternalHigh', ULONG_PTR),
            ('_offset_union', _OFFSET_UNION),
            ('hEvent', HANDLE)]


    LPOVERLAPPED = POINTER(OVERLAPPED)

    # --- Define function prototypes for extra safety ---
    LockFileEx = windll.kernel32.LockFileEx
    LockFileEx.restype = BOOL
    LockFileEx.argtypes = [HANDLE, DWORD, DWORD, DWORD, DWORD, LPOVERLAPPED]
    UnlockFileEx = windll.kernel32.UnlockFileEx
    UnlockFileEx.restype = BOOL
    UnlockFileEx.argtypes = [HANDLE, DWORD, DWORD, DWORD, LPOVERLAPPED]


    def flock(file_, flags):
        hfile = msvcrt.get_osfhandle(file_.fileno())
        overlapped = OVERLAPPED()
        if flags & LOCK_UN and UnlockFileEx(hfile, 0, 0, 0xFFFF0000, byref(overlapped)):
            return
        elif (not flags or flags & (LOCK_EX | LOCK_NB | LOCK_SH)) and \
                LockFileEx(hfile, flags, 0, 0, 0xFFFF0000, byref(overlapped)):
            return
        raise IOError(GetLastError())

else:
    from fcntl import flock, LOCK_EX, LOCK_NB, LOCK_SH, LOCK_UN


class FileSemaphore(file):

    def __init__(self, name, mode='rb', buffering=-1):
        self.locked = False
        super(FileSemaphore, self).__init__(name, mode, buffering)

    def lockex(self, nb=False):
        flags = LOCK_EX
        if nb:
            flags |= LOCK_NB
        flock(self, flags)
        self.locked = True

    def locksh(self, nb=False):
        flags = LOCK_SH
        if nb:
            flags |= LOCK_NB
        flock(self, flags)
        self.locked = True

    def unlock(self, nb=False):
        flags = LOCK_UN
        if nb:
            flags |= LOCK_NB
        flock(self, flags)
        self.locked = False

    def __del__(self):
        if self.locked and not self.closed:
            self.unlock()

    def close(self):
        super(FileSemaphore, self).close()
        if self.locked and not self.closed:
            self.unlock()

    def __exit__(self, *args):
        super(FileSemaphore, self).__exit__(*args)
        if self.locked and not self.closed:
            self.unlock()


class FileMutex(FileSemaphore):

    def __init__(self, name):
        super(FileMutex, self).__init__(os.path.join(gettempdir(), name), 'wb')
        self.lockex()


def UniqueFile(self, name, delete=False):
    n, e = os.path.splitext(name)
    f = NamedTemporaryFile(suffix=e, prefix='%s_' % n, delete=delete)
    if os.name == 'posix':
        os.chmod(f.name, 0644)
    return f


class PushDir(object):
    """Ripped from here: https://gist.github.com/Tatsh/7131812"""

    def __init__(self, dir_name):
        self.cwd = os.path.realpath(dir_name)
        self.original_dir = None

    def __enter__(self):
        self.original_dir = os.getcwd()
        if os.path.lexists(self.cwd):
            os.chdir(self.cwd)
        else:
            sys.stderr.write('WARNING: %r directory does not exist. Falling back to %r.' %
                             (self.cwd, self.original_dir))
        return self

    def __exit__(self, type_, value, tb):
        os.chdir(self.original_dir)


class CookieFile(FileSemaphore):

    @property
    def age(self):
        return time() - os.stat(self.name).st_mtime

    @property
    def expired(self):
        return self.age > self.max_age

    def __init__(self, name, mode='rb', buffering=-1, max_age=86400):
        name = os.path.join(gettempdir(), name)
        self.max_age = max_age
        super(CookieFile, self).__init__(name, mode, buffering=-1)

        if 'w' in self.mode:
            self.lockex()
        elif 'r' in self.mode:
            self.locksh()
            if self.expired:
                self.close()
                raise IOError('Cookie file expired (age=%d > max_age=%d).' % (self.age, max_age))
