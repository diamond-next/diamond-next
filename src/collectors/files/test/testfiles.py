#!/usr/bin/python3
# coding=utf-8

import unittest

from collectors.files.files import FilesCollector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestFilesCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config("FilesCollector", {})
        self.collector = FilesCollector(config, None)

    def test_import(self):
        self.assertTrue(FilesCollector)


if __name__ == "__main__":
    unittest.main()
