#!/usr/bin/python
# coding=utf-8

import unittest

from collectors.puppetdb.puppetdb import PuppetDBCollector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestPuppetDBCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('PuppetDBCollector', {
            'interval': 10
        })

        self.collector = PuppetDBCollector(config, None)

    def test_import(self):
        self.assertTrue(PuppetDBCollector)


if __name__ == "__main__":
    unittest.main()
