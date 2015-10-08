import zlib
import re
import urllib

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2015, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'wordlist'
]


def wordlist(uri, match='(.+?)\n*', ignore='^#.*', strip=None):
    if isinstance(uri, basestring):
        l = []
        if not uri:
            return l
        data = urllib.urlopen(uri).read()
        if re.search('\.gz(ip)?$', uri) is not None:
            data = zlib.decompress(data, 16 + zlib.MAX_WBITS)
        if data:
            if callable(match):
                l = match(data)
            else:
                l = re.findall(match, data)
                if ignore is not None:
                    l = filter(lambda x: re.search(ignore, x) is None, l)
                if strip is not None:
                    l = map(lambda x: re.sub(strip, '', x), l)
        return l
    return uri
