import unittest
from argparse import Namespace
from os import getcwd, makedirs, walk, rmdir, remove
from os.path import dirname, join, realpath, exists

import simplejson as json
import tests.tests_core.test_data as td
from expan.cli.cli import check_input_data, UsageError, prepare_cli_parameters, parse_metadata, run_analysis

__location__ = realpath(join(getcwd(), dirname(__file__)))

TEST_FOLDER = __location__ + '/test_folder'


class CliTestCase(unittest.TestCase):
	def setUp(self):
		# create test folder
		if not exists(TEST_FOLDER):
			makedirs(TEST_FOLDER)

		# generate metrics and metadata
		(metrics, metadata) = td.generate_random_data()

		# save features to .csv.gz file in test folder
		metrics.to_csv(path_or_buf=TEST_FOLDER + '/features.csv.gz', compression='gzip')

		# save kpis to .csv.gz file in test folder
		metrics.to_csv(path_or_buf=TEST_FOLDER + '/kpis.csv.gz', compression='gzip')

		# save metadata to .json file in test folder
		with open(TEST_FOLDER + '/metadata.json', 'w') as f:
			json.dump(metadata, f)

	def tearDown(self):
		# remove all test files and test folder
		for root, dirs, files in walk(TEST_FOLDER, topdown=False):
			for name in files:
				remove(join(root, name))
			for name in dirs:
				rmdir(join(root, name))
		rmdir(TEST_FOLDER)

	def test_check_input_data(self):
		args = Namespace(kpis=False, metadata=False)
		self.assertRaises(UsageError, check_input_data, args)

		args = Namespace(kpis='bla', metadata=False)
		self.assertRaises(UsageError, check_input_data, args)

		args = Namespace(kpis='bla', metadata='bla')
		self.assertIsNone(check_input_data(args=args))

	def test_prepare_cli_parameters(self):
		args = Namespace(kpis='kpis_file', features='features_file', metadata='metadata_file', output='output_file')
		self.assertTupleEqual(prepare_cli_parameters(args),
							  ('features_file', 'kpis_file', 'metadata_file', 'output_file'))

	def test_run_analysis(self):
		run_analysis(features_file=None,
					 kpis_file=TEST_FOLDER + '/kpis.csv.gz',
					 metadata_file=TEST_FOLDER + '/metadata.json')

	def test_parse_metadata(self):
		# print(parse_metadata(TEST_FOLDER + '/metadata.json'))
		self.assertDictEqual(parse_metadata(TEST_FOLDER + '/metadata.json'),
							 {'source': 'simulated',
							  'primary_KPI': 'normal_shifted',
							  'experiment': 'random_data_generation',
							  'baseline_variant': 'A'})
