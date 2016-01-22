import unittest

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2015, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

if __name__ == "__main__":
    all_tests = unittest.TestLoader().discover('canari.unittests', pattern='*.py')
    unittest.TextTestRunner().run(all_tests)
