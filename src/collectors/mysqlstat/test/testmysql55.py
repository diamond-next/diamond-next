#!/usr/bin/python3
# coding=utf-8

from collectors.mysqlstat.mysql55 import MySQLPerfCollector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestMySQLPerfCollector(CollectorTestCase):
    def setUp(self, allowed_names=None):
        if not allowed_names:
            allowed_names = []

        config = get_collector_config(
            "MySQLPerfCollector", {"allowed_names": allowed_names, "interval": 1}
        )
        self.collector = MySQLPerfCollector(config, None)

    def test_import(self):
        self.assertTrue(MySQLPerfCollector)
