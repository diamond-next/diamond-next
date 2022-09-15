# coding=utf-8

"""
Collect metrics from Puppet Dashboard

#### Dependencies

 * urllib

"""

import re
import urllib.request

import diamond.collector


class PuppetDashboardCollector(diamond.collector.Collector):
    def get_default_config_help(self):
        config_help = super(PuppetDashboardCollector, self).get_default_config_help()
        config_help.update(
            {
                "host": "Hostname to collect from",
                "port": "Port number to collect from",
                "path": "Path to the dashboard",
            }
        )
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(PuppetDashboardCollector, self).get_default_config()
        config.update(
            {
                "host": "localhost",
                "port": 5678,
                "path": "puppetdashboard",
            }
        )
        return config

    def collect(self):
        try:
            response = urllib.request.urlopen(
                "http://%s:%s/" % (self.config["host"], int(self.config["port"]))
            )
        except Exception as e:
            self.log.error("Could not connect to puppet-dashboard: %s", e)
            return {}

        for line in response.readlines():
            line = line.strip()

            if line == "":
                continue

            try:
                regex = re.compile(
                    '<a href="/nodes/(?P<key>[\w.]+)">(?P<count>[\d.]+)</a>'
                )
                r = regex.search(line)
                results = r.groupdict()

                self.publish(results["key"], results["count"])
            except Exception as e:
                self.log.error("Could not parse the output: %s", e)
