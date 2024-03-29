#!/usr/bin/python3
# coding=utf-8

import io
import unittest
from unittest.mock import Mock, patch

from collectors.proc.proc import ProcessStatCollector
from diamond.collector import Collector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestProcessStatCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config("ProcessStatCollector", {"interval": 1})

        self.collector = ProcessStatCollector(config, None)

    def test_import(self):
        self.assertTrue(ProcessStatCollector)

    @patch("builtins.open")
    @patch("os.access", Mock(return_value=True))
    @patch.object(Collector, "publish")
    def test_should_open_proc_stat(self, publish_mock, open_mock):
        open_mock.return_value = io.StringIO("")
        self.collector.collect()
        open_mock.assert_called_once_with("/proc/stat", "r")

    @patch.object(Collector, "publish")
    def test_should_work_with_real_data(self, publish_mock):
        ProcessStatCollector.PROC = self.getFixturePath("proc_stat_1")
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        ProcessStatCollector.PROC = self.getFixturePath("proc_stat_2")
        self.collector.collect()

        metrics = {
            "ctxt": 1791,
            "btime": 1319181102,
            "processes": 2,
            "procs_running": 1,
            "procs_blocked": 0,
        }

        self.setDocExample(
            collector=self.collector.__class__.__name__,
            metrics=metrics,
            defaultpath=self.collector.config["path"],
        )
        self.assertPublishedMany(publish_mock, metrics)


if __name__ == "__main__":
    unittest.main()
