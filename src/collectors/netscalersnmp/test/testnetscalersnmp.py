#!/usr/bin/python3
# coding=utf-8

from collectors.netscalersnmp.netscalersnmp import NetscalerSNMPCollector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestNetscalerSNMPCollector(CollectorTestCase):
    def setUp(self, allowed_names=None):
        if not allowed_names:
            allowed_names = []

        config = get_collector_config(
            "NetscalerSNMPCollector", {"allowed_names": allowed_names, "interval": 1}
        )
        self.collector = NetscalerSNMPCollector(config, None)

    def test_import(self):
        self.assertTrue(NetscalerSNMPCollector)
