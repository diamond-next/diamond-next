#!/usr/bin/python3
# coding=utf-8

import unittest

from collectors.vmsfs.vmsfs import VMSFSCollector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestVMSFSCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config("VMSFSCollector", {})
        self.collector = VMSFSCollector(config, None)

    def test_import(self):
        self.assertTrue(VMSFSCollector)


if __name__ == "__main__":
    unittest.main()
