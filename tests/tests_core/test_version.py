import runpy
import unittest

from expan.core.version import version, version_numbers, git_commit_count, git_latest_commit


class VersionTestCase(unittest.TestCase):
	@staticmethod
	def test_main():
		runpy.run_module('expan.core.version', run_name='__main__')

	def test_version(self):
		self.assertIn('v', version())
		self.assertIn('Short Version String: "v', version('Short Version String: "{short}"'))
		self.assertIn('Full Version String: "v', version('Full Version String: "{long}"'))

	def test_version_numbers(self):
		self.assertEqual(len(version_numbers()), 3)

	def test_git_commit_count(self):
		self.assertTrue(git_commit_count())

	def test_git_latest_commit(self):
		self.assertEqual(len(git_latest_commit()), 40)
