#!/usr/bin/python
# coding=utf-8

import unittest
from collections import Iterator
from unittest.mock import Mock, call, patch

from collectors.sockstat.sockstat import SockstatCollector
from diamond.collector import Collector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestSockstatCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('SockstatCollector', {
            'interval': 10
        })

        self.collector = SockstatCollector(config, None)

    def test_import(self):
        self.assertTrue(SockstatCollector)

    @patch('builtins.open')
    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_open_proc_net_sockstat(self, publish_mock, open_mock):
        class Klass(Iterator):
            def close(self):
                pass

            def next(self):
                raise StopIteration

        open_mock.return_value = Klass()
        self.collector.collect()
        calls = [call('/proc/net/sockstat'), call('/proc/net/sockstat6')]
        open_mock.assert_has_calls(calls)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        SockstatCollector.PROCS = [self.getFixturePath('proc_net_sockstat'),
                                   self.getFixturePath('proc_net_sockstat6')]
        self.collector.collect()

        metrics = {
            'used': 118,
            'tcp_inuse': 61,
            'tcp_orphan': 0,
            'tcp_tw': 1,
            'tcp_alloc': 13,
            'tcp_mem': 1,
            'udp_inuse': 6,
            'udp_mem': 0
        }

        self.setDocExample(collector=self.collector.__class__.__name__, metrics=metrics, defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)


if __name__ == "__main__":
    unittest.main()
