# coding=utf-8

"""
The SNMPInterfaceCollector is designed for collecting interface data from
remote SNMP-enabled devices such as routers and switches using SNMP IF_MIB

#### Installation

The snmpinterfacecollector.py module should be installed into your Diamond
installation collectors directory. This directory is defined
in diamond.cfg under the *collectors_path* directive. This defaults to
*/usr/share/diamond/collectors/* on Ubuntu.

The SNMPInterfaceCollector.cfg file should be installed into your diamond
installation config directory. This directory is defined
in diamond.cfg under the *collectors_config_path* directive. This defaults to
*/etc/diamond/* on Ubuntu.

Once the collector is installed and configured, you can wait for diamond to
pick up the new collector automatically, or simply restart diamond.

#### Configuration

Below is an example configuration for the SNMPInterfaceCollector. The collector
can collect data any number of devices by adding configuration sections
under the *devices* header. By default the collector will collect every 60
seconds. This might be a bit excessive and put unnecessary load on the
devices being polled. You may wish to change this to every 300 seconds. However
you need modify your graphite data retentions to handle this properly.

```
    # Options for SNMPInterfaceCollector
    path = interface
    interval = 60

    [devices]

    [[router1]]
    host = router1.example.com
    port = 161
    community = public

    [[router2]]
    host = router1.example.com
    port = 161
    community = public
```

Note: If you modify the SNMPInterfaceCollector configuration, you will need to
restart diamond.

#### Dependencies

 * pysmnp

#### Notes

This implimentation is well suited for collecting a small number of metrics
locally. If you want to collect a large number of remote metrics, consider
https://github.com/GreggBzz/snmp-interface-poll as an alternative collector

"""

import os
import re

import sys

import diamond.convertor

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'snmp'))

from snmp import SNMPCollector as parent_SNMPCollector


class SNMPInterfaceCollector(parent_SNMPCollector):
    # IF-MIB OID
    IF_MIB_INDEX_OID = "1.3.6.1.2.1.2.2.1.1"
    IF_MIB_NAME_OID = "1.3.6.1.2.1.31.1.1.1.1"
    IF_MIB_TYPE_OID = "1.3.6.1.2.1.2.2.1.3"

    # A list of IF-MIB 32bit counters to walk
    IF_MIB_GAUGE_OID_TABLE = {'ifInDiscards': "1.3.6.1.2.1.2.2.1.13",
                              'ifInErrors': "1.3.6.1.2.1.2.2.1.14",
                              'ifOutDiscards': "1.3.6.1.2.1.2.2.1.19",
                              'ifOutErrors': "1.3.6.1.2.1.2.2.1.20"}

    # A list of IF-MIB 64bit counters to talk
    IF_MIB_COUNTER_OID_TABLE = {'ifHCInOctets': "1.3.6.1.2.1.31.1.1.1.6",
                                'ifInUcastPkts': "1.3.6.1.2.1.31.1.1.1.7",
                                'ifInMulticastPkts': "1.3.6.1.2.1.31.1.1.1.8",
                                'ifInBroadcastPkts': "1.3.6.1.2.1.31.1.1.1.9",
                                'ifHCOutOctets': "1.3.6.1.2.1.31.1.1.1.10",
                                'ifOutUcastPkts': "1.3.6.1.2.1.31.1.1.1.11",
                                'ifOutMulticastPkts': "1.3.6.1.2.1.31.1.1.1.12",
                                'ifOutBroadcastPkts': "1.3.6.1.2.1.31.1.1.1.13"}

    # A list of interface types we care about
    IF_TYPES = ["6"]

    def get_default_config_help(self):
        config_help = super(SNMPInterfaceCollector, self).get_default_config_help()
        config_help.update({})

        return config_help

    def get_default_config(self):
        """
        Override SNMPCollector.get_default_config method to provide
        default_config for the SNMPInterfaceCollector
        """
        default_config = super(SNMPInterfaceCollector, self).get_default_config()
        default_config['path'] = 'interface'
        default_config['byte_unit'] = ['bit', 'byte']
        return default_config

    def collect_snmp(self, device, host, port, community):
        """
        Collect SNMP interface data from device
        """
        # Log
        self.log.info("Collecting SNMP interface statistics from: %s", device)

        # Get Interface Indexes
        if_index_oid = '.'.join([self.IF_MIB_INDEX_OID])
        if_index_data = self.walk(if_index_oid, host, port, community)

        # Define a list of interface indexes
        if_indexes = [v for v in if_index_data.values()]

        for ifIndex in if_indexes:
            # Get Interface Type
            if_type_oid = '.'.join([self.IF_MIB_TYPE_OID, ifIndex])
            if_type_data = self.get(if_type_oid, host, port, community)

            if if_type_data[if_type_oid] not in self.IF_TYPES:
                # Skip Interface
                continue

            # Get Interface Name
            if_name_oid = '.'.join([self.IF_MIB_NAME_OID, ifIndex])
            if_name_data = self.get(if_name_oid, host, port, community)
            if_name = if_name_data[if_name_oid]

            # Remove quotes from string
            if_name = re.sub(r'(\"|\')', '', if_name)

            # Get Gauges
            for gaugeName, gaugeOid in self.IF_MIB_GAUGE_OID_TABLE.items():
                if_gauge_oid = '.'.join([self.IF_MIB_GAUGE_OID_TABLE[gaugeName], ifIndex])
                if_gauge_data = self.get(if_gauge_oid, host, port, community)
                if_gauge_value = if_gauge_data[if_gauge_oid]

                if not if_gauge_value:
                    continue

                # Get Metric Name and Value
                metric_if_descr = re.sub(r'\W', '_', if_name)
                metric_name = '.'.join([metric_if_descr, gaugeName])
                metric_value = int(if_gauge_value)

                # Get Metric Path
                metric_path = '.'.join(['devices', device, self.config['path'], metric_name])

                # Publish Metric
                self.publish_gauge(metric_path, metric_value)

            # Get counters (64bit)
            counter_items = self.IF_MIB_COUNTER_OID_TABLE.items()

            for counterName, counterOid in counter_items:
                if_counter_oid = '.'.join([self.IF_MIB_COUNTER_OID_TABLE[counterName], ifIndex])
                if_counter_data = self.get(if_counter_oid, host, port, community)
                if_counter_value = if_counter_data[if_counter_oid]

                if not if_counter_value:
                    continue

                # Get Metric Name and Value
                metric_if_descr = re.sub(r'\W', '_', if_name)

                if counterName in ['ifHCInOctets', 'ifHCOutOctets']:
                    for unit in self.config['byte_unit']:
                        # Convert Metric
                        metric_name = '.'.join([metric_if_descr, counterName.replace('Octets', unit)])
                        metric_value = diamond.convertor.binary.convert(value=if_counter_value, old_unit='byte', new_unit=unit)

                        # Get Metric Path
                        metric_path = '.'.join(['devices', device, self.config['path'], metric_name])

                        # Publish Metric
                        self.publish_counter(metric_path, metric_value, max_value=18446744073709600000)
                else:
                    metric_name = '.'.join([metric_if_descr, counterName])
                    metric_value = int(if_counter_value)

                    # Get Metric Path
                    metric_path = '.'.join(['devices', device, self.config['path'], metric_name])

                    # Publish Metric
                    self.publish_counter(metric_path, metric_value, max_value=18446744073709600000)
