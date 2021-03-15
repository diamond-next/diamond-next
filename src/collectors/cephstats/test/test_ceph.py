#!/usr/bin/env python

import os
import sys
import unittest

from collectors.cephstats.cephstats import process_ceph_status

curdir = os.path.dirname(os.path.abspath(__file__))
os.chdir(curdir)
sys.path.insert(0, '../')
sys.path.insert(0, '../../ceph')


class TestCephStats(unittest.TestCase):
    """
    Test collect ceph data
    """
    def test_sample_data(self):
        """
        Get ceph information from sample data
        """
        f = open('sample.txt')
        ret = {'rd': '8643000.0', 'wr': '4821000.0', 'iops': '481'}
        self.assertEqual(process_ceph_status(f.read()), ret)
        f.close()

    def test_sample_data_noio(self):
        """
        Get ceph information from sample data, missing the 'client io'
        """
        f = open('sample-noio.txt')
        self.assertEqual(process_ceph_status(f.read()), {})
        f.close()


if __name__ == '__main__':
    unittest.main()
