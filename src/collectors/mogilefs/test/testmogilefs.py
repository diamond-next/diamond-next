#!/usr/bin/python3
# coding=utf-8

import unittest
from unittest.mock import Mock, patch

from collectors.mogilefs.mogilefs import MogilefsCollector
from diamond.collector import Collector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestMogilefsCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config("MogilefsCollector", {"interval": 10})

        self.collector = MogilefsCollector(config, None)

    def test_import(self):
        self.assertTrue(MogilefsCollector)

    @patch.object(Collector, "publish")
    def test_stub_data(self, publish_mock):
        mock_telnet = Mock(
            **{"read_until.return_value": self.getFixture("stats").getvalue()}
        )
        patch_telnet = patch("telnetlib.Telnet", Mock(return_value=mock_telnet))

        patch_telnet.start()
        self.collector.collect()
        patch_telnet.stop()

        mock_telnet.read_until.assert_any_call(".", 3)

        metrics = {
            "uptime": 181491,
            "pending_queries": 0,
            "processing_queries": 1,
            "bored_queryworkers": 49,
            "queries": 4353158,
            "times_out_of_qworkers": 2,
            "work_queue_for_delete": 2,
            "work_queue_for_replicate": 0,
            "work_sent_to_delete": 336154,
            "work_sent_to_replicate": 274882,
        }

        self.assertPublishedMany(publish_mock, metrics)


if __name__ == "__main__":
    unittest.main()
