# coding=utf-8
"""
Gather HTTP Response code and Duration of HTTP request

#### Dependencies
  * urllib
"""

import time
from datetime import datetime
from urllib.error import URLError
from urllib.request import Request, urlopen

from diamond.collector import Collector


class WebsiteMonitorCollector(Collector):
    """
    Gather HTTP response code and Duration of HTTP request
    """
    def get_default_config_help(self):
        config_help = super(WebsiteMonitorCollector, self).get_default_config_help()
        config_help.update({
            'URL': "FQDN of HTTP endpoint to test",
        })

        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        default_config = super(WebsiteMonitorCollector, self).get_default_config()
        default_config['URL'] = ''
        default_config['path'] = 'websitemonitor'

        return default_config

    def collect(self):
        req = Request('%s' % (self.config['URL']))

        # time in seconds since epoch as a floating number
        start_time = time.time()

        try:
            # human-readable time e.g November 25, 2013 18:15:56
            st = datetime.fromtimestamp(start_time).strftime('%B %d, %Y %H:%M:%S')
            self.log.debug('Start time: %s' % st)

            resp = urlopen(req)

            # time in seconds since epoch as a floating number
            end_time = time.time()

            # human-readable end time e.eg. November 25, 2013 18:15:56
            et = datetime.fromtimestamp(end_time).strftime('%B %d, %Y %H:%M%S')
            self.log.debug('End time: %s' % et)

            # Response time in milliseconds
            rt = int(format((end_time - start_time) * 1000, '.0f'))

            # Publish metrics
            self.publish('response_time.%s' % resp.code, rt, metric_type='COUNTER')
        # urllib will puke on non HTTP 200/OK URLs
        except URLError as e:
            if e.code != 200:
                # time in seconds since epoch as a floating number
                end_time = time.time()

                # Response time in milliseconds
                rt = int(format((end_time - start_time) * 1000, '.0f'))

                # Publish metrics -- this is recording a failure, rt will likely be 0 but does capture HTTP Status Code
                self.publish('response_time.%s' % e.code, rt, metric_type='COUNTER')

        except IOError:
            self.log.error('Unable to open %s' % (self.config['URL']))

        except Exception as e:
            self.log.error("Unknown error opening url: %s", e)
