#!/usr/bin/python3
# coding=utf-8

import unittest

from collectors.celerymon.celerymon import CelerymonCollector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestCelerymonCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config("CelerymonCollector", {})
        self.collector = CelerymonCollector(config, None)

    def test_import(self):
        self.assertTrue(CelerymonCollector)


if __name__ == "__main__":
    unittest.main()
