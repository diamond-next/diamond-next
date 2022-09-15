#!/usr/bin/python3
# coding=utf-8

import unittest

from collectors.netapp.netappDisk import netappDisk
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestnetappDisk(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('netappDisk', {})
        self.collector = netappDisk(config, None)

    def test_import(self):
        self.assertTrue(netappDisk)


if __name__ == "__main__":
    unittest.main()
