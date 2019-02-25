from __future__ import print_function
import os
import inspect
import configobj
import unittest

try:
    import cPickle as pickle
except ImportError:
    import pickle as pickle

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

try:
    from setproctitle import setproctitle
except ImportError:
    setproctitle = None


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


class CollectorTestCase(unittest.TestCase):

    def setDocExample(self, collector, metrics, defaultpath=None):
        # function does not fit in to test case
        return

    def getFixtureDirPath(self):
        path = os.path.join(
            os.path.dirname(inspect.getfile(self.__class__)),
            'fixtures')
        return path

    def getFixturePath(self, fixture_name):
        path = os.path.join(self.getFixtureDirPath(),
                            fixture_name)
        if not os.access(path, os.R_OK):
            print("Missing Fixture " + path)
        return path

    def getFixture(self, fixture_name):
        with open(self.getFixturePath(fixture_name), 'r') as f:
            return StringIO(f.read())

    def getFixtures(self):
        fixtures = []
        for root, dirnames, filenames in os.walk(self.getFixtureDirPath()):
            fixtures.append(os.path.join(root, dirnames, filenames))
        return fixtures

    def getPickledResults(self, results_name):
        with open(self.getFixturePath(results_name), 'r') as f:
            return pickle.load(f)

    def setPickledResults(self, results_name, data):
        with open(self.getFixturePath(results_name), 'w+b') as f:
            pickle.dump(data, f)

    def assertUnpublished(self, mock, key, value, expected_value=0):
        return self.assertPublished(mock, key, value, expected_value)

    def assertPublished(self, mock, key, value, expected_value=1):
        if type(mock) is list:
            for m in mock:
                calls = (filter(lambda x: x[0][0] == key, m.call_args_list))
                if len(calls) > 0:
                    break
        else:
            calls = filter(lambda x: x[0][0] == key, mock.call_args_list)

        actual_value = len(calls)
        message = '%s: actual number of calls %d, expected %d' % (
            key, actual_value, expected_value)

        self.assertEqual(actual_value, expected_value, message)

        if expected_value:
            actual_value = calls[0][0][1]
            expected_value = value
            precision = 0

            if isinstance(value, tuple):
                expected_value, precision = expected_value

            message = '%s: actual %r, expected %r' % (key,
                                                      actual_value,
                                                      expected_value)

            if precision is not None:
                self.assertAlmostEqual(float(actual_value),
                                       float(expected_value),
                                       places=precision,
                                       msg=message)
            else:
                self.assertEqual(actual_value, expected_value, message)

    def assertUnpublishedMany(self, mock, dict, expected_value=0):
        return self.assertPublishedMany(mock, dict, expected_value)

    def assertPublishedMany(self, mock, dict, expected_value=1):
        for key, value in dict.iteritems():
            self.assertPublished(mock, key, value, expected_value)

        if type(mock) is list:
            for m in mock:
                m.reset_mock()
        else:
            mock.reset_mock()

    def assertUnpublishedMetric(self, mock, key, value, expected_value=0):
        return self.assertPublishedMetric(mock, key, value, expected_value)

    def assertPublishedMetric(self, mock, key, value, expected_value=1):
        calls = filter(lambda x: x[0][0].path.find(key) != -1,
                       mock.call_args_list)

        actual_value = len(calls)
        message = '%s: actual number of calls %d, expected %d' % (
            key, actual_value, expected_value)

        self.assertEqual(actual_value, expected_value, message)

        if expected_value:
            actual_value = calls[0][0][0].value
            expected_value = value
            precision = 0

            if isinstance(value, tuple):
                expected_value, precision = expected_value

            message = '%s: actual %r, expected %r' % (key,
                                                      actual_value,
                                                      expected_value)

            if precision is not None:
                self.assertAlmostEqual(float(actual_value),
                                       float(expected_value),
                                       places=precision,
                                       msg=message)
            else:
                self.assertEqual(actual_value, expected_value, message)

    def assertUnpublishedMetricMany(self, mock, dict, expected_value=0):
        return self.assertPublishedMetricMany(mock, dict, expected_value)

    def assertPublishedMetricMany(self, mock, dict, expected_value=1):
        for key, value in dict.iteritems():
            self.assertPublishedMetric(mock, key, value, expected_value)

        mock.reset_mock()
