#!/usr/bin/python
# coding=utf-8

import unittest

from collectors.s3.s3 import S3BucketCollector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestS3BucketCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('S3BucketCollector', {
            'interval': 10
        })

        self.collector = S3BucketCollector(config, None)

    def test_import(self):
        self.assertTrue(S3BucketCollector)


if __name__ == "__main__":
    unittest.main()
