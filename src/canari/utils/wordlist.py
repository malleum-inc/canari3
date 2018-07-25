from future.standard_library import install_aliases
from six import string_types

install_aliases()

import zlib
import re
from urllib.request import urlopen

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


def wordlist(uri, match='(.+?)\n*', ignore='^#.*', strip=None):
    if isinstance(uri, string_types):
        words = []
        if not uri:
            return words
        data = urlopen(uri).read()
        if re.search('\.gz(ip)?$', uri) is not None:
            data = zlib.decompress(data, 16 + zlib.MAX_WBITS)
        if data:
            if callable(match):
                words = match(data)
            else:
                words = re.findall(match, data.decode('utf-8'))
                if ignore is not None:
                    words = [w for w in words if re.search(ignore, w) is None]
                if strip is not None:
                    words = map(lambda x: re.sub(strip, '', x), words)
        return words
    return uri
