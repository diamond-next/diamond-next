#!/usr/bin/python3
# coding=utf-8

import unittest
from unittest.mock import Mock, patch

from collectors.supervisord.supervisord import SupervisordCollector
from diamond.collector import Collector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestSupervisordCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('SupervisordCollector', {})
        self.collector = SupervisordCollector(config, None)
        self.assertTrue(self.collector)

    def test_import(self):
        self.assertTrue(SupervisordCollector)

    @patch.object(Collector, 'publish')
    def test_success(self, publish_mock):
        self.collector.get_all_process_info = Mock(return_value=eval(self.getFixture('valid_fixture').getvalue()))

        self.collector.collect()

        metrics = {
            'test_group.test_name_1.state': 20,
            'test_group.test_name_1.uptime':  5,
            'test_group.test_name_2.state': 200,
            'test_group.test_name_2.uptime': 500
        }

        self.setDocExample(collector=self.collector.__class__.__name__, metrics=metrics, defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)


if __name__ == "__main__":
    unittest.main()
