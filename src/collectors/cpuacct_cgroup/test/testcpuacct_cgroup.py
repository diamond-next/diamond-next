#!/usr/bin/python
# coding=utf-8

import io
import os
import unittest
from unittest.mock import patch

from collectors.cpuacct_cgroup.cpuacct_cgroup import CpuAcctCgroupCollector
from diamond.collector import Collector
from diamond.testing import CollectorTestCase
from test import get_collector_config


class TestCpuAcctCgroupCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('CpuAcctCgroupCollector', {
            'interval': 10
        })

        self.collector = CpuAcctCgroupCollector(config, None)

    def test_import(self):
        self.assertTrue(CpuAcctCgroupCollector)

    @patch('builtins.open')
    @patch.object(Collector, 'publish')
    def test_should_open_all_cpuacct_stat(self, publish_mock, open_mock):
        return
        self.collector.config['path'] = self.getFixtureDirPath()
        open_mock.side_effect = lambda x: io.StringIO('')
        self.collector.collect()

        # All the fixtures we should be opening
        paths = [
            'lxc/testcontainer/cpuacct.stat',
            'lxc/cpuacct.stat',
            'cpuacct.stat',
        ]

        for path in paths:
            open_mock.assert_any_call(os.path.join(
                self.getFixtureDirPath(), path))

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        self.collector.config['path'] = self.getFixtureDirPath()
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'lxc.testcontainer.user': 1318,
            'lxc.testcontainer.system': 332,
            'lxc.user': 36891,
            'lxc.system': 88927,
            'system.user': 3781253,
            'system.system': 4784004,
        })


if __name__ == "__main__":
    unittest.main()
