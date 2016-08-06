__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2016, canari Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = []


def parse_bool(question, default=True):
    choices = 'Y/n' if default else 'y/N'
    default = 'Y' if default else 'N'
    while True:
        ans = raw_input('%s [%s]: ' % (question, choices)).upper() or default
        if ans.startswith('Y'):
            return True
        elif ans.startswith('N'):
            return False
        else:
            print('Invalid selection (%s) must be either [y]es or [n]o.' % ans)


def parse_int(question, choices, default=0):
    while True:
        for i, c in enumerate(choices):
            print('[%d] - %s' % (i, c))
        ans = raw_input('%s [%d]: ' % (question, default)) or default
        try:
            ans = int(ans)
            if not 0 <= ans <= i:
                raise ValueError
            return ans
        except ValueError:
            print('Invalid selection (%s) must be an integer between 0 and %d.' % (ans, i))


def parse_int_range(question, from_, to, default=0):
    from_ = int(from_)
    to = int(to)

    if from_ > to:
        temp = from_
        from_ = to
        to = temp

    while True:
        ans = parse_str('%s. Valid values are between %d and %d' % (question, from_, to), default)
        try:
            ans = int(ans)
            if not from_ <= ans <= to:
                raise ValueError
            return ans
        except ValueError:
            print('Invalid selection (%s) must be an integer between %d and %d.' % (ans, from_, to))


def parse_str(question, default):
    return raw_input('%s [%s]: ' % (question, default)) or default