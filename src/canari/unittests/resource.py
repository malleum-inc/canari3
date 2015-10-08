from unittest import TestCase
from canari.resource import *
import os

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2015, Canari Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


class ResourceTests(TestCase):

    def test_external_resource(self):
        resource = external_resource('wordlist.txt', 'canari.unittests.resources')
        self.assertTrue(resource.endswith('canari/unittests/resources/wordlist.txt'))
        self.assertTrue(os.path.lexists(resource))

    def test_image_resource(self):
        icon = image_resource('0.png', 'canari.unittests.resources.images')
        self.assertTrue(icon.startswith('/') and icon.endswith('canari/unittests/resources/images/0.png'))
        self.assertTrue(os.path.lexists(icon))

    def test_icon_resource(self):
        icon = icon_resource('0.png', 'canari.unittests.resources.images')
        self.assertTrue(icon.startswith('file:///') and icon.endswith('canari/unittests/resources/images/0.png'))
        self.assertTrue(os.path.lexists(icon.replace('file://', '')))

    def test_image_resources(self):
        images = image_resources('canari.unittests')
        self.assertTrue(images)
        self.assertTrue(len(images) == 4)
        for i, j in enumerate(images):
            self.assertTrue(j.endswith('canari/unittests/resources/images/%d.png' % i))
            self.assertTrue(os.path.lexists(j))

    def test_conf(self):
        self.assertTrue(conf, 'Configuration file path could not be determined.')
        self.assertTrue(conf.endswith('canari/resources/etc/canari.conf'))
        self.assertTrue(os.path.lexists(conf))