# coding=utf-8

"""
SNMPCollector for Server Tech PDUs

Server Tech is a manufacturer of PDUs
http://www.servertech.com/

"""

import os
import re

import sys
import time

import diamond.metric

# Fix Path for locating the SNMPCollector
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../", "snmp")))

from snmp import SNMPCollector as parent_SNMPCollector


class ServerTechPDUCollector(parent_SNMPCollector):
    """
    SNMPCollector for ServerTech PDUs
    """

    PDU_SYSTEM_GAUGES = {"systemTotalWatts": "1.3.6.1.4.1.1718.3.1.6"}

    PDU_INFEED_NAMES = "1.3.6.1.4.1.1718.3.2.2.1.3"

    PDU_INFEED_GAUGES = {
        "infeedCapacityAmps": "1.3.6.1.4.1.1718.3.2.2.1.10",
        "infeedVolts": "1.3.6.1.4.1.1718.3.2.2.1.11",
        "infeedAmps": "1.3.6.1.4.1.1718.3.2.2.1.7",
        "infeedWatts": "1.3.6.1.4.1.1718.3.2.2.1.12",
    }

    def get_default_config_help(self):
        config_help = super(ServerTechPDUCollector, self).get_default_config_help()
        config_help.update(
            {
                "host": "PDU dns address",
                "port": "PDU port to collect snmp data",
                "community": "SNMP community",
            }
        )
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(ServerTechPDUCollector, self).get_default_config()
        config.update(
            {
                "path": "pdu",
                "timeout": 15,
                "retries": 3,
            }
        )
        return config

    def collect_snmp(self, device, host, port, community):
        """
        Collect stats from device
        """
        # Log
        self.log.info("Collecting ServerTech PDU statistics from: %s" % device)

        # Set timestamp
        timestamp = time.time()

        input_feeds = {}

        # Collect PDU input gauge values
        for gaugeName, gaugeOid in self.PDU_SYSTEM_GAUGES.items():
            system_gauges = self.walk(gaugeOid, host, port, community)

            for o, gaugeValue in system_gauges.items():
                # Get Metric Name
                metric_name = gaugeName

                # Get Metric Value
                metric_value = float(gaugeValue)

                # Get Metric Path
                metric_path = ".".join(["devices", device, "system", metric_name])

                # Create Metric
                metric = diamond.metric.Metric(metric_path, metric_value, timestamp, 2)

                # Publish Metric
                self.publish_metric(metric)

        # Collect PDU input feed names
        input_feed_names = self.walk(self.PDU_INFEED_NAMES, host, port, community)

        for o, inputFeedName in input_feed_names.items():
            # Extract input feed name
            input_feed = ".".join(o.split(".")[-2:])
            input_feeds[input_feed] = inputFeedName

        # Collect PDU input gauge values
        for gaugeName, gaugeOid in self.PDU_INFEED_GAUGES.items():
            input_feed_gauges = self.walk(gaugeOid, host, port, community)

            for o, gaugeValue in input_feed_gauges.items():
                # Extract input feed name
                input_feed = ".".join(o.split(".")[-2:])

                # Get Metric Name
                metric_name = ".".join(
                    [re.sub(r"\.|\\", "_", input_feeds[input_feed]), gaugeName]
                )

                # Get Metric Value
                if gaugeName == "infeedVolts":
                    # Note: Voltage is in "tenth volts", so divide by 10
                    metric_value = float(gaugeValue) / 10.0
                elif gaugeName == "infeedAmps":
                    # Note: Amps is in "hundredth amps", so divide by 100
                    metric_value = float(gaugeValue) / 100.0
                else:
                    metric_value = float(gaugeValue)

                # Get Metric Path
                metric_path = ".".join(["devices", device, "input", metric_name])

                # Create Metric
                metric = diamond.metric.Metric(metric_path, metric_value, timestamp, 2)

                # Publish Metric
                self.publish_metric(metric)
