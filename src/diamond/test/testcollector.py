#!/usr/bin/python
# coding=utf-8

import unittest
from unittest.mock import patch

import configobj

from diamond.collector import Collector


class BaseCollectorTest(unittest.TestCase):
    def test_SetCustomHostname(self):
        config = configobj.ConfigObj()
        config['server'] = {}
        config['server']['collectors_config_path'] = ''
        config['collectors'] = {}
        config['collectors']['collectorsDefault'] = {
            'hostname': 'custom.localhost',
        }
        c = Collector(config, [])
        self.assertEquals('custom.localhost', c.get_hostname())

    def test_SetHostnameViaShellCmd(self):
        config = configobj.ConfigObj()
        config['server'] = {}
        config['server']['collectors_config_path'] = ''
        config['collectors'] = {}
        config['collectors']['collectorsDefault'] = {
            'hostname': 'echo custom.localhost',
            'hostname_method': 'shell',
        }
        c = Collector(config, [])
        self.assertEquals(b'custom.localhost', c.get_hostname())

    @patch('diamond.collector.get_hostname')
    def test_get_metric_path_no_prefix(self, get_hostname_mock):
        config = configobj.ConfigObj()
        config['collectors'] = {}
        config['collectors']['collectorsDefault'] = {}
        config['collectors']['collectorsDefault']['path_prefix'] = ''
        config['collectors']['collectorsDefault']['path'] = 'bar'

        get_hostname_mock.return_value = None

        result = Collector(config, []).get_metric_path('foo')

        self.assertEqual('bar.foo', result)

    @patch('diamond.collector.get_hostname')
    def test_get_metric_path_no_prefix_no_path(self, get_hostname_mock):
        config = configobj.ConfigObj()
        config['collectors'] = {}
        config['collectors']['collectorsDefault'] = {}
        config['collectors']['collectorsDefault']['path_prefix'] = ''
        config['collectors']['collectorsDefault']['path'] = ''

        get_hostname_mock.return_value = None

        result = Collector(config, []).get_metric_path('foo')

        self.assertEqual('foo', result)

    @patch('diamond.collector.get_hostname')
    def test_get_metric_path_no_path(self, get_hostname_mock):
        config = configobj.ConfigObj()
        config['collectors'] = {}
        config['collectors']['collectorsDefault'] = {}
        config['collectors']['collectorsDefault']['path_prefix'] = 'bar'
        config['collectors']['collectorsDefault']['path'] = ''

        get_hostname_mock.return_value = None

        result = Collector(config, []).get_metric_path('foo')

        self.assertEqual('bar.foo', result)

    @patch('diamond.collector.get_hostname')
    def test_get_metric_path_dot_path(self, get_hostname_mock):
        config = configobj.ConfigObj()
        config['collectors'] = {}
        config['collectors']['collectorsDefault'] = {}
        config['collectors']['collectorsDefault']['path_prefix'] = 'bar'
        config['collectors']['collectorsDefault']['path'] = '.'

        get_hostname_mock.return_value = None

        result = Collector(config, []).get_metric_path('foo')

        self.assertEqual('bar.foo', result)

    @patch('diamond.collector.get_hostname')
    def test_get_metric_path(self, get_hostname_mock):
        config = configobj.ConfigObj()
        config['collectors'] = {}
        config['collectors']['collectorsDefault'] = {}
        config['collectors']['collectorsDefault']['path_prefix'] = 'poof'
        config['collectors']['collectorsDefault']['path'] = 'xyz'

        get_hostname_mock.return_value = 'bar'

        result = Collector(config, []).get_metric_path('foo')

        self.assertEqual('poof.bar.xyz.foo', result)
