#!/usr/bin/python
# coding=utf-8

import unittest
from unittest.mock import Mock, patch

from collectors.http.http import HttpCollector
from diamond.collector import Collector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestHttpCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('HttpCollector', {
            'req_vhost': 'www.my_server.com',
            'req_url': ['http://www.my_server.com/']
        })

        self.collector = HttpCollector(config, None)

    def test_import(self):
        self.assertTrue(HttpCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        patch_urlopen = patch('urllib.request.urlopen', Mock(return_value=self.getFixture('index')))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        metrics = {
            'http__www_my_server_com_.size': 150,
        }

        self.setDocExample(collector=self.collector.__class__.__name__, metrics=metrics, defaultpath=self.collector.config['path'])
        self.assertPublishedMany([publish_mock], metrics)


if __name__ == "__main__":
    unittest.main()
