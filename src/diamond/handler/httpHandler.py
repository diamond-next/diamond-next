#!/usr/bin/env python
# coding=utf-8

"""
Send metrics to a http endpoint via POST
"""

import urllib.request

import diamond.handler.Handler


class HttpPostHandler(diamond.handler.Handler.Handler):
    # Inititalize Handler with url and batch size
    def __init__(self, config=None):
        diamond.handler.Handler.Handler.__init__(self, config)
        self.metrics = []
        self.batch_size = int(self.config['batch'])
        self.url = self.config.get('url')

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this handler
        """
        config = super(HttpPostHandler, self).get_default_config_help()

        config.update({
            'url': 'Fully qualified url to send metrics to',
            'batch': 'How many to store before sending to the graphite server',
        })

        return config

    def get_default_config(self):
        """
        Return the default config for the handler
        """
        config = super(HttpPostHandler, self).get_default_config()

        config.update({
            'url': 'http://localhost/blah/blah/blah',
            'batch': 100,
        })

        return config

    # Join batched metrics and push to url mentioned in config
    def process(self, metric):
        self.metrics.append(str(metric))

        if len(self.metrics) >= self.batch_size:
            self.post()

    # Overriding flush to post metrics for every collector.
    def flush(self):
        """Flush metrics in queue"""
        self.post()

    def post(self):
        req = urllib.request.Request(self.url, b"\n".join(self.metrics))
        urllib.request.urlopen(req)
        self.metrics = []
