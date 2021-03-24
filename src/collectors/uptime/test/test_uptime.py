#!/usr/bin/python
# coding=utf-8

import io
from unittest.mock import Mock, patch

from collectors.uptime.uptime import UptimeCollector
from diamond.collector import Collector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestUptimeCollector(CollectorTestCase):
    def setUp(self, config=None):
        if config is None:
            config = get_collector_config('UptimeCollector', {
                'interval': '10',
            })
        else:
            config = get_collector_config('UptimeCollector', config)

        self.collector = UptimeCollector(config, None)

    def test_import(self):
        self.assertTrue(UptimeCollector)

    @patch('builtins.open')
    @patch('os.path.exists', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_open_proc_uptime(self, publish_mock, open_mock):
        open_mock.return_value = io.StringIO('1288459.83 10036802.26')
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/uptime')

    @patch.object(Collector, 'publish')
    def test_sanity_check(self, publish_mock):
        self.collector.PROC = self.getFixturePath('sanity_check')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'minutes': 60
        })

    @patch.object(Collector, 'publish')
    def test_malformed_input(self, publish_mock):
        self.collector.PROC = self.getFixturePath('malformed_input')
        self.collector.collect()
        self.collector.PROC = self.getFixturePath('sanity_check')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'minutes': 60.0
        })

    @patch.object(Collector, 'publish')
    def test_seconds(self, publish_mock):
        self.setUp(config={
            'interval': '10',
            'metric_name': 'seconds',
        })
        self.collector.PROC = self.getFixturePath('sanity_check')
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'seconds': 3600
        })
