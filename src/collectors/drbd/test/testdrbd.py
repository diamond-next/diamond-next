#!/usr/bin/python
# coding=utf-8

import unittest

from collectors.drbd.drbd import DRBDCollector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestDRBDCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('DRBDCollector', {})

        self.collector = DRBDCollector(config, None)

    def test_import(self):
        self.assertTrue(DRBDCollector)


if __name__ == "__main__":
    unittest.main()
