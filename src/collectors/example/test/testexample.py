#!/usr/bin/python
# coding=utf-8

import unittest
from unittest.mock import patch

from collectors.example.example import ExampleCollector
from diamond.collector import Collector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestExampleCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('ExampleCollector', {
            'interval': 10
        })

        self.collector = ExampleCollector(config, None)

    def test_import(self):
        self.assertTrue(ExampleCollector)

    @patch.object(Collector, 'publish')
    def test(self, publish_mock):
        self.collector.collect()

        metrics = {
            'my.example.metric':  42
        }

        self.setDocExample(collector=self.collector.__class__.__name__, metrics=metrics, defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)


if __name__ == "__main__":
    unittest.main()
