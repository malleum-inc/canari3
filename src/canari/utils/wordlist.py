from six import string_types
from six.moves.urllib import request

import zlib
import re

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2015, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@redcanari.com'
__status__ = 'Development'

__all__ = [
    'wordlist'
]


def wordlist(uri, match='(.+?)[\n\r]*', ignore='^\s*#.*', strip=None, decompressor=None):
    if isinstance(uri, string_types):
        words = []
        if not uri:
            return words
        data = request.urlopen(uri).read()

        if decompressor:
            data = decompressor(data)
        elif uri.endswith(('.gz', '.gzip')):
            data = zlib.decompress(data, 16 + zlib.MAX_WBITS)

        if data:
            if callable(match):
                words = match(data)
            else:
                words = re.findall(match, data.decode('utf-8'))
                if ignore:
                    if isinstance(ignore, str):
                        ignore = re.compile(ignore).search
                    words = [w for w in words if not ignore(w) and w]
                if strip:
                    if isinstance(strip, str):
                        strip = re.compile(strip).sub
                    words = [strip('', w) for w in words]
        return words
    return uri
