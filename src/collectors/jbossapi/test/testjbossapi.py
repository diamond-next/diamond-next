#!/usr/bin/python3
# coding=utf-8

import unittest

from collectors.jbossapi.jbossapi import JbossApiCollector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestJbossApiCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config("JbossApiCollector", {})
        self.collector = JbossApiCollector(config, None)

    def test_import(self):
        self.assertTrue(JbossApiCollector)


if __name__ == "__main__":
    unittest.main()
