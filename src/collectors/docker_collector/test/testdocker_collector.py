#!/usr/bin/python
# coding=utf-8

import json
import os
import unittest

from collectors.docker_collector.docker_collector import DockerCollector
from diamond.testing import CollectorTestCase
from test import get_collector_config, run_only

try:
    from docker import Client
except ImportError:
    Client = None

dirname = os.path.dirname(__file__)
fixtures_path = os.path.join(dirname, 'fixtures/')


def run_only_if_docker_client_is_available(func):
    try:
        from docker import Client
    except ImportError:
        Client = None

    pred = lambda: Client is not None

    return run_only(func, pred)


class TestDockerCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('DockerCollector', {
            'interval': 10,
        })

        self.collector = DockerCollector(config, None)

    def test_import(self):
        self.assertTrue(DockerCollector)

    def test_docker_stats_method_exists(self):
        self.assertTrue("stats" in dir(Client))

    def test_docker_stats_output_parse(self):
        f = open(os.path.join(fixtures_path, "example.stat")).read()
        stat = json.loads(f)

        for path in self.collector.METRICS:
            val = self.collector.get_value(path, stat)
            self.assertTrue(val is not None)

    def test_docker_stats_output_parse_fail(self):
        f = open(os.path.join(fixtures_path, "example_empty.stat")).read()
        stat = json.loads(f)

        for path in self.collector.METRICS:
            val = self.collector.get_value(path, stat)
            self.assertTrue(val is None)


if __name__ == "__main__":
    unittest.main()
