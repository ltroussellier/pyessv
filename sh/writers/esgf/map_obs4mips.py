# -*- coding: utf-8 -*-

"""
.. module:: map_obs4mips.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps obs4MIPs ESGF publisher ini file to normalized pyessv format.

.. moduleauthor:: Mark Conway_Greenslade <momipsl@ipsl.jussieu.fr>

"""
from utils import yield_comma_delimited_options


# Vocabulary collections extracted from ini file.
COLLECTIONS = [
	('product', yield_comma_delimited_options),
	('institute', yield_comma_delimited_options),
	('realm', yield_comma_delimited_options),
	('var', yield_comma_delimited_options),
	('variable', lambda: yield_variable),
	('time_frequency', yield_comma_delimited_options),
	('data_structure', yield_comma_delimited_options),
	('source_id', yield_comma_delimited_options),
	('dataset_version', r'latest|^v[0-9]*$'),
	('processing_level', r'^[A-Za-z0-9]*$'),
	('processing_version', r'^[A-Za-z0-9]*$'),
	('las_time_delta', lambda: yield_las_time_delta),
	('thredds_exclude_variables', yield_comma_delimited_options),
	('file_period', r'fixed|^\d+-\d+(-clim)?$')
]

# Fields extracted from ini file & appended as data to the scope.
SCOPE_DATA = {
	'filename': {
		'template': '{}_{}_{}_{}_{}',
    	'collections': (
			'variable',
			'source_id',
			'processing_level',
			'processing_version',
			'file_period'
			)
	},
	'directory_structure': {
		'template': 'obs4MIPs/{}/{}/{}/{}/{}/{}/{}/{}',
		'collections': (
			'product',
			'realm',
			'var',
			'time_frequency',
			'data_structure',
			'institute',
			'source_id',
			'dataset_version'
			)
	},
	'dataset_id': {
		'template': 'obs4MIPs.{}.{}.{}.{}.{}',
		'collections': (
			'institute',
			'source_id',
			'variable',
			'time_frequency',
			'dataset_version'
			)
	}
}


def yield_variable(ctx):
	"""Yields institute information to be converted to pyessv terms.

	"""
	for var, variable in ctx.ini_section.get_option('variable_map', '\n', '|'):
		src_namespace = 'wcrp:obs4mips:var:{}'.format(var.lower().replace('_','-'))
		yield src_namespace, variable


def yield_las_time_delta(ctx):
	"""Yields las time delta information to be converted to pyessv terms.

	"""
	for time_frequency, las_time_delta in ctx.ini_section.get_option('las_time_delta_map', '\n', '|'):
		src_namespace = 'wcrp:obs4mips:time-frequency:{}'.format(time_frequency.lower().replace('_', '-'))
		yield src_namespace, las_time_delta
