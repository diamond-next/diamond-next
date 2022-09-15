#!/usr/bin/python3
# coding=utf-8

from collectors.openldap.openldap import OpenLDAPCollector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestOpenLDAPCollector(CollectorTestCase):
    def setUp(self, allowed_names=None):
        if not allowed_names:
            allowed_names = []

        config = get_collector_config("OpenLDAPCollector", {})
        self.collector = OpenLDAPCollector(config, None)

    def test_import(self):
        self.assertTrue(OpenLDAPCollector)
