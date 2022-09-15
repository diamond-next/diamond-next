#!/usr/bin/python3
# coding=utf-8

import unittest
from unittest.mock import Mock, patch

from collectors.aurora.aurora import AuroraCollector
from diamond.collector import Collector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestAuroraCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config("AuroraCollector", {})

        self.collector = AuroraCollector(config, None)

    def test_import(self):
        self.assertTrue(AuroraCollector)

    @patch.object(Collector, "publish")
    def test_should_work_with_real_data(self, publish_mock):
        def se(url):
            if url == "http://localhost:8081/vars":
                return self.getFixture("metrics")

        patch_urlopen = patch("urllib.request.urlopen", Mock(side_effect=se))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        metrics = self.get_metrics()

        self.setDocExample(
            collector=self.collector.__class__.__name__,
            metrics=metrics,
            defaultpath=self.collector.config["path"],
        )
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, "publish")
    def test_should_fail_gracefully(self, publish_mock):
        patch_urlopen = patch(
            "urllib.request.urlopen",
            Mock(return_value=self.getFixture("metrics_blank")),
        )

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        self.assertPublishedMany(publish_mock, {})

    def get_metrics(self):
        return {
            "async.tasks.completed": 11117.0,
            "attribute.store.fetch.all.events": 24.0,
            "attribute.store.fetch.all.events.per.sec": 0.0,
            "attribute.store.fetch.all.nanos.per.event": 0.0,
            "attribute.store.fetch.all.nanos.total": 90208119.0,
            "attribute.store.fetch.all.nanos.total.per.sec": 0.0,
            "attribute.store.fetch.one.events": 33024.0,
            "tasks.FAILED.computers.prod.computer-traffic-analysis": 517.0,
            "tasks.FAILED.reporting.prod.report-processing": 2.0,
        }


if __name__ == "__main__":
    unittest.main()
