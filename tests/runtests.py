# -*- coding: utf-8 -*-
import argparse
import sys
import os
import unittest

DIR_PATH = os.path.dirname(__file__)


def runtests():

    parser = argparse.ArgumentParser(
        description='Run the devappserver2 test suite.'
    )
    parser.add_argument(
        'tests',
        nargs='*',
        help='The fully qualified names of the tests to run (e.g. '
        'test_email_client). If not given '
        'then the full test suite will be run.',
    )
    args = parser.parse_args()
    loader = unittest.TestLoader()
    if args.tests:
        tests = loader.loadTestsFromNames(args.tests)
    else:
        tests = loader.discover(DIR_PATH, 'test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(tests)


if __name__ == '__main__':
    package_path = os.path.join(DIR_PATH, '..')
    sys.path.insert(0, os.path.abspath(package_path))
    runtests()
