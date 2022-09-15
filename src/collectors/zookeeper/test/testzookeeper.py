#!/usr/bin/python3
# coding=utf-8

import unittest

from collectors.zookeeper.zookeeper import ZookeeperCollector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestZookeeperCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config("ZookeeperCollector", {})
        self.collector = ZookeeperCollector(config, None)

    def test_import(self):
        self.assertTrue(ZookeeperCollector)


if __name__ == "__main__":
    unittest.main()
