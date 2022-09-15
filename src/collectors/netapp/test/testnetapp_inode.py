#!/usr/bin/python3
# coding=utf-8

import unittest

from collectors.netapp.netapp_inode import netapp_inode
from diamond.testing import CollectorTestCase
from test import get_collector_config


class Testnetapp_inode(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('netapp_inode', {})
        self.collector = netapp_inode(config, None)

    def test_import(self):
        self.assertTrue(netapp_inode)


if __name__ == "__main__":
    unittest.main()
