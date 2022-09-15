#!/usr/bin/python3
# coding=utf-8

import io
import unittest
from unittest.mock import Mock, patch

from collectors.memory.memory import MemoryCollector
from diamond.collector import Collector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestMemoryCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('MemoryCollector', {
            'interval': 10,
            'byte_unit': 'kilobyte'
        })

        self.collector = MemoryCollector(config, None)

    def test_import(self):
        self.assertTrue(MemoryCollector)

    @patch('builtins.open')
    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_open_proc_meminfo(self, publish_mock, open_mock):
        open_mock.return_value = io.StringIO('')
        self.collector.collect()
        open_mock.assert_called_once_with('/proc/meminfo')

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        MemoryCollector.PROC = self.getFixturePath('proc_meminfo')
        self.collector.collect()

        metrics = {
            'MemTotal': 49554212,
            'MemFree': 35194496,
            'MemAvailable': 35194496,
            'MemUsedPercentage': 28.98,
            'Buffers': 1526304,
            'Cached': 10726736,
            'Active': 10022168,
            'Dirty': 24748,
            'Inactive': 2524928,
            'Shmem': 276,
            'SwapTotal': 262143996,
            'SwapFree': 262143996,
            'SwapCached': 0,
            'VmallocTotal': 34359738367,
            'VmallocUsed': 445452,
            'VmallocChunk': 34311049240
        }

        self.setDocExample(collector=self.collector.__class__.__name__, metrics=metrics, defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)


if __name__ == "__main__":
    unittest.main()
