#!/usr/bin/python3
# coding=utf-8

import os
import unittest
from unittest.mock import patch

from collectors.hadoop.hadoop import HadoopCollector
from diamond.collector import Collector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestHadoopCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config(
            "HadoopCollector",
            {
                "metrics": [os.path.dirname(__file__) + "/fixtures/*metrics.log"],
            },
        )

        self.collector = HadoopCollector(config, {})

    def test_import(self):
        self.assertTrue(HadoopCollector)

    @patch.object(Collector, "publish_metric")
    def test_should_work_with_real_data(self, publish_mock):
        self.collector.collect()

        metrics = self.getPickledResults("expected.pkl")

        self.setDocExample(
            collector=self.collector.__class__.__name__,
            metrics=metrics,
            defaultpath=self.collector.config["path"],
        )
        self.assertPublishedMetricMany(publish_mock, metrics)


if __name__ == "__main__":
    unittest.main()
