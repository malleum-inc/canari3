# import getpass
# import os
# import random
# import shutil
# import sys
# from unittest import TestCase
#
# from click.testing import CliRunner
# from pkg_resources import resource_filename
#
# from canari.entrypoints import main
# from canari.pkgutils.transform import TransformDistribution
# from canari.utils.fs import PushDir
#
#
# class DispatcherTests(TestCase):
#
#     def run(self, *args, **kwargs):
#         cli = CliRunner(env=os.environ)
#         self.package_name = 'foo_%d' % random.randint(0, 100)
#         with cli.isolated_filesystem():
#             result = cli.invoke(main, ('create-package', self.package_name), input='\n\nfoo@bar.com\n', env=os.environ)
#             assert result.exit_code == 0
#             with PushDir(os.path.join(self.package_name, 'src')):
#                 super(DispatcherTests, self).run(*args, **kwargs)
#
#     def test_non_existent_package_name(self):
#         self.assertRaises(ImportError, TransformDistribution, 'bar')
#
#     def test_non_canari_package_name(self):
#         self.assertRaises(ImportError, TransformDistribution, 'click')
#
#     def test_canari_package_with_no_resources_folder(self):
#         shutil.rmtree(os.path.join(self.package_name, 'resources'))
#         self.assertListEqual([], TransformDistribution(self.package_name).machines)
#
#     def test_empty_canari_package(self):
#         os.unlink(os.path.join(self.package_name, 'transforms', 'helloworld.py'))
#         self.assertRaises(ValueError, TransformDistribution, self.package_name)
#
#     def test_transform_distribution_read(self):
#         dist = TransformDistribution(self.package_name)
#         self.assertEqual(self.package_name, dist.name)
#         self.assertEqual(getpass.getuser(), dist.author)
#         self.assertEqual('foo@bar.com', dist.author_email)
#         self.assertListEqual(['HelloWorld'], [t.__name__ for t in dist.transforms])
#         self.assertEqual('%s.conf' % self.package_name, dist.config_file)
#         self.assertListEqual(['%sEntity' %  self.package_name.title(), 'My%sEntity' % self.package_name.title()],
#                              sorted([e.__name__ for e in dist.entities]))
#         self.assertEqual(os.getcwd(), dist.default_prefix)
#         self.assertEqual(resource_filename('%s.resources.maltego' % self.package_name, 'entities.mtz'),
#                          dist.entities_file)
#         self.assertTrue(dist.has_transforms)
#         self.assertFalse(dist.has_remote_transforms)
#         self.assertFalse(dist.is_site_package)
#         self.assertListEqual([], dist.machines)
#         self.assertListEqual([], dist.remote_transforms)
#         self.assertEqual(os.path.join(os.getcwd(), self.package_name), dist.package_path)
#         self.assertEqual(resource_filename('%s.resources.maltego' % self.package_name, 'profile.mtz'),
#                          dist.profile_file)
#         self.assertEqual('%s.resources' % self.package_name, dist.resources)
#
