#!/usr/bin/python3
# coding=utf-8

import unittest

from collectors.entropy.entropy import EntropyStatCollector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestEntropyStatCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config("EntropyStatCollector", {})

        self.collector = EntropyStatCollector(config, None)

    def test_import(self):
        self.assertTrue(EntropyStatCollector)


if __name__ == "__main__":
    unittest.main()
