# coding=utf-8

"""
Collect Uptime metrics

#### Dependencies

    * /proc/uptime

"""

import os

from diamond import convertor
from diamond.collector import Collector


class UptimeCollector(Collector):
    PROC = '/proc/uptime'

    def get_default_config(self):
        config = super(UptimeCollector, self).get_default_config()
        config.update({
            'path': 'uptime',
            'metric_name': 'minutes'
        })
        return config

    def collect(self):
        if not os.path.exists(self.PROC):
            self.log.error('Input path %s does not exist' % self.PROC)
            return {}

        v = self.read()

        if v is not None:
            self.publish(self.config['metric_name'], v)

    def read(self):
        try:
            fd = open(self.PROC)
            uptime = fd.readline()
            fd.close()
            v = float(uptime.split()[0].strip())

            return convertor.time.convert(v, 's', self.config['metric_name'])
        except Exception as e:
            self.log.error('Unable to read uptime from %s: %s' % (self.PROC, e))
            return None
