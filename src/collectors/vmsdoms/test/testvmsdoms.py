#!/usr/bin/python
# coding=utf-8

import unittest

from collectors.vmsdoms.vmsdoms import VMSDomsCollector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestVMSDomsCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('VMSDomsCollector', {})
        self.collector = VMSDomsCollector(config, None)

    def test_import(self):
        self.assertTrue(VMSDomsCollector)


if __name__ == "__main__":
    unittest.main()
