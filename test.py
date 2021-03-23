#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function

import inspect
import logging
import optparse
import os
import sys
import traceback
import unittest

import configobj

try:
    from setproctitle import setproctitle
except ImportError:
    setproctitle = None

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src', 'collectors')))


def run_only(func, predicate):
    if predicate():
        return func
    else:
        def f(arg):
            pass

        return f


def get_collector_config(key, value):
    config = configobj.ConfigObj()
    config['server'] = {}
    config['server']['collectors_config_path'] = ''
    config['collectors'] = {}
    config['collectors']['default'] = {}
    config['collectors']['default']['hostname_method'] = "uname_short"
    config['collectors'][key] = value

    return config


collectorTests = {}


def get_collector_tests(path, verbose=True):
    for f in os.listdir(path):
        fn = os.path.abspath(os.path.join(path, f))

        if os.path.isfile(fn) and f.startswith('test') and f.endswith('.py'):
            sys.path.append(os.path.dirname(fn))
            sys.path.append(os.path.dirname(os.path.dirname(fn)))
            modname = f[:-3]

            try:
                # Import the module
                collectorTests[modname] = __import__(modname, globals(), locals(), ['*'])
            except Exception:
                print("Failed to import module: %s." % (modname, ))
                print("Traceback: %s" % (traceback.format_exc(), ))
                continue

    for f in os.listdir(path):
        fn = os.path.abspath(os.path.join(path, f))

        if os.path.isdir(fn):
            get_collector_tests(fn)


if __name__ == "__main__":
    if setproctitle:
        setproctitle('test.py')

    # Disable log output for the unit tests
    log = logging.getLogger("diamond")
    log.addHandler(logging.StreamHandler(sys.stderr))
    log.disabled = True

    # Initialize Options
    parser = optparse.OptionParser()
    parser.add_option("-c", "--collector", dest="collector", default="", help="Run a single collector's unit tests")
    parser.add_option("-v", "--verbose", dest="verbose", default=1, action="count", help="verbose")

    # Parse Command Line Args
    (options, args) = parser.parse_args()

    cPath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src', 'collectors', options.collector))

    dPath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src', 'diamond'))

    get_collector_tests(cPath, options.verbose)

    if not options.collector:
        # Only pull in diamond tests when a specific collector hasn't been specified
        get_collector_tests(dPath)

    loader = unittest.TestLoader()
    tests = []

    for test in collectorTests:
        for name, c in inspect.getmembers(collectorTests[test], inspect.isclass):
            if not issubclass(c, unittest.TestCase):
                continue

            tests.append(loader.loadTestsFromTestCase(c))

    suite = unittest.TestSuite(tests)
    results = unittest.TextTestRunner(verbosity=options.verbose).run(suite)

    results = str(results)
    results = results.replace('>', '').split()[1:]
    resobj = {}

    for result in results:
        result = result.split('=')
        resobj[result[0]] = int(result[1])

    if resobj['failures'] > 0:
        sys.exit(1)

    if resobj['errors'] > 0:
        sys.exit(2)

    sys.exit(0)
