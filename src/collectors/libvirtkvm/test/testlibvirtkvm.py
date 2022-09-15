#!/usr/bin/python3
# coding=utf-8

import unittest

from collectors.libvirtkvm.libvirtkvm import LibvirtKVMCollector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestLibvirtKVMCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config("LibvirtKVMCollector", {})
        self.collector = LibvirtKVMCollector(config, None)

    def test_import(self):
        self.assertTrue(LibvirtKVMCollector)


if __name__ == "__main__":
    unittest.main()
