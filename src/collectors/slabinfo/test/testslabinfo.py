#!/usr/bin/python
# coding=utf-8

import io
import unittest
from unittest.mock import Mock, patch

from collectors.slabinfo.slabinfo import SlabInfoCollector
from diamond.collector import Collector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestSlabInfoCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('SlabInfoCollector', {
            'interval': 1
        })

        self.collector = SlabInfoCollector(config, None)

    def test_import(self):
        self.assertTrue(SlabInfoCollector)

    @patch('builtins.open')
    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_open_proc_stat(self, publish_mock, open_mock):
        open_mock.return_value = io.StringIO('')
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/slabinfo', 'r')

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        SlabInfoCollector.PROC = self.getFixturePath('slabinfo')
        self.collector.collect()

        metrics = self.getPickledResults('expected.pkl')

        self.setDocExample(collector=self.collector.__class__.__name__, metrics=metrics, defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)


if __name__ == "__main__":
    unittest.main()
