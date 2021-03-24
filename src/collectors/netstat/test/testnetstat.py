#!/usr/bin/python
# coding=utf-8

from __future__ import print_function

import unittest
from unittest.mock import patch

from collectors.netstat.netstat import NetstatCollector
from diamond.collector import Collector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestNetstatCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('NetstatCollector', {})

        self.collector = NetstatCollector(config, None)

    @patch.object(Collector, 'publish')
    def test(self, publish_mock):
        NetstatCollector.PROC_TCP = self.getFixturePath('proc_net_tcp')
        self.collector.collect()

        metrics = {
            'LISTEN': 9
        }

        self.setDocExample(collector=self.collector.__class__.__name__, metrics=metrics, defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)


if __name__ == "__main__":
    unittest.main()
