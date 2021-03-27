#!/usr/bin/python3
# coding=utf-8

import unittest

from collectors.sqs.sqs import SqsCollector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestSqsCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('SqsCollector', {})
        self.collector = SqsCollector(config, None)

    def test_import(self):
        self.assertTrue(SqsCollector)


if __name__ == "__main__":
    unittest.main()
