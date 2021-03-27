#!/usr/bin/python3
# coding=utf-8

import unittest
from unittest.mock import Mock, patch

from collectors.numa.numa import NumaCollector
from diamond.collector import Collector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestNumaCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('NumaCollector', {
            'interval': 10,
            'bin': 'true'
        })

        self.collector = NumaCollector(config, None)

    def test_import(self):
        self.assertTrue(NumaCollector)

    @patch.object(Collector, 'publish')
    def test(self, publish_mock):
        self.collector.collect()

        metrics = {
            'node_0_free_MB': 342,
            'node_0_size_MB': 15976
        }

        patch_communicate = patch('subprocess.Popen.communicate', Mock(return_value=(self.getFixture('single_node.txt').getvalue(), '')))
        patch_communicate.start()
        self.collector.collect()
        patch_communicate.stop()

        self.setDocExample(collector=self.collector.__class__.__name__, metrics=metrics, defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)


if __name__ == "__main__":
    unittest.main()
