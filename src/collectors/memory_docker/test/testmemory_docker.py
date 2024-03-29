#!/usr/bin/python3
# coding=utf-8

import io
import os
import unittest
from unittest.mock import Mock, patch

from diamond.collector import Collector
from diamond.testing import CollectorTestCase
from test import get_collector_config, run_only

try:
    from docker import Client
except ImportError:
    Client = None

from memory_docker import MemoryDockerCollector

fixtures_path = os.path.join(os.path.dirname(__file__), "fixtures/")
fixtures = []

for root, dirnames, filenames in os.walk(fixtures_path):
    fixtures.append([root, dirnames, filenames])

docker_fixture = [
    {
        "Id": "c3341726a9b4235a35b390c5f6f28e5a6869879a48da1d609db8f6bf4275bdc5",
        "Names": ["/testcontainer"],
    },
    {
        "Id": "9c151939e20682b924d7299875e94a4aabbe946b30b407f89e276507432c625b",
        "Names": None,
    },
]


def run_only_if_docker_client_is_available(func):
    try:
        from docker import Client
    except ImportError:
        Client = None

    pred = lambda: Client is not None

    return run_only(func, pred)


class TestMemoryDockerCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config(
            "MemoryDockerCollector",
            {
                "interval": 10,
                "byte_unit": "megabyte",
                "memory_path": fixtures_path,
            },
        )

        self.collector = MemoryDockerCollector(config, None)

    def test_import(self):
        self.assertTrue(MemoryDockerCollector)

    @run_only_if_docker_client_is_available
    @patch("builtins.open")
    @patch.object(Client, "containers", Mock(return_value=[]))
    @patch.object(Collector, "publish")
    def test_should_open_all_cpuacct_stat(self, publish_mock, open_mock):
        open_mock.side_effect = lambda x: io.StringIO("")
        self.collector.collect()
        open_mock.assert_any_call(fixtures_path + "lxc/testcontainer/memory.stat")
        open_mock.assert_any_call(fixtures_path + "lxc/memory.stat")
        open_mock.assert_any_call(fixtures_path + "memory.stat")

    @run_only_if_docker_client_is_available
    @patch("builtins.open")
    @patch.object(Client, "containers")
    @patch.object(Collector, "publish")
    def test_should_get_containers(self, publish_mock, containers_mock, open_mock):
        containers_mock.return_value = []
        open_mock.side_effect = lambda x: io.StringIO("")
        self.collector.collect()
        containers_mock.assert_any_call(all=True)

    @run_only_if_docker_client_is_available
    @patch.object(Collector, "publish")
    @patch.object(Client, "containers", Mock(return_value=docker_fixture))
    def test_should_work_with_real_data(self, publish_mock):
        self.collector.collect()

        self.assertPublishedMany(
            publish_mock,
            {
                "lxc.testcontainer.cache": 1,
                "lxc.testcontainer.rss": 1,
                "lxc.testcontainer.swap": 1,
                "lxc.cache": 1,
                "lxc.rss": 1,
                "lxc.swap": 1,
                "system.cache": 1,
                "system.rss": 1,
                "system.swap": 1,
                "docker.testcontainer.cache": 1,
                "docker.testcontainer.rss": 1,
                "docker.testcontainer.swap": 1,
                "docker.cache": 1,
                "docker.rss": 1,
                "docker.swap": 1,
            },
        )


if __name__ == "__main__":
    unittest.main()
