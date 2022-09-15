#!/usr/bin/python3
# coding=utf-8

import unittest

from collectors.netapp.netapp import NetAppCollector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestNetAppCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config("NetAppCollector", {})
        self.collector = NetAppCollector(config, None)

    def test_import(self):
        self.assertTrue(NetAppCollector)


if __name__ == "__main__":
    unittest.main()
