#!/usr/bin/python
# coding=utf-8

import unittest

from collectors.passenger_stats.passenger_stats import PassengerCollector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestPassengerCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('PassengerCollector', {})
        self.collector = PassengerCollector(config, None)

    def test_import(self):
        self.assertTrue(PassengerCollector)


if __name__ == "__main__":
    unittest.main()
