#!/usr/bin/python3
# coding=utf-8

from collectors.ossec.ossec import OssecCollector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestOssecCollector(CollectorTestCase):
    def setUp(self, allowed_names=None):
        if not allowed_names:
            allowed_names = []

        config = get_collector_config("OssecCollector", {})
        self.collector = OssecCollector(config, None)

    def test_import(self):
        self.assertTrue(OssecCollector)
