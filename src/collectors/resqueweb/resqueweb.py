# coding=utf-8

"""
Collects data for Resque Web

#### Dependencies

 * urllib

"""

from urllib.request import urlopen

from diamond.collector import Collector


class ResqueWebCollector(Collector):
    def get_default_config_help(self):
        config_help = super(ResqueWebCollector, self).get_default_config_help()
        config_help.update({})
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(ResqueWebCollector, self).get_default_config()
        config.update({
            'host': 'localhost',
            'port': 5678,
            'path': 'resqueweb',
        })
        return config

    def collect(self):
        try:
            response = urlopen("http://%s:%s/stats.txt" % (self.config['host'], int(self.config['port'])))
        except Exception as e:
            self.log.error('Could not connect to resque-web: %s', e)
            return {}

        for data in response.read().split("\n"):
            if data == "":
                continue

            item, count = data.strip().split("=")

            try:
                count = int(count)
                (item, queue) = item.split(".")

                if item == "resque":
                    if queue[-1] == "+":
                        self.publish("%s.total" % queue.replace("+", ""), count)
                    else:
                        self.publish("%s.current" % queue, count)
                else:
                    self.publish("queue.%s.current" % queue, count)

            except Exception as e:
                self.log.error('Could not parse the queue: %s', e)
