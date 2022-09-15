#!/usr/bin/python3
# coding=utf-8

from unittest.mock import Mock, patch

from collectors.httpjson.httpjson import HTTPJSONCollector
from diamond.collector import Collector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestHTTPJSONCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('HTTPJSONCollector', {})
        self.collector = HTTPJSONCollector(config, None)

    def test_import(self):
        self.assertTrue(HTTPJSONCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        urlopen_mock = patch('urllib.request.urlopen', Mock(return_value=self.getFixture('stats.json')))

        urlopen_mock.start()
        self.collector.collect()
        urlopen_mock.stop()

        metrics = self.getPickledResults("real_stat.pkl")

        self.assertPublishedMany(publish_mock, metrics)
