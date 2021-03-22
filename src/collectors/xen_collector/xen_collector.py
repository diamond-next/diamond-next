# coding=utf-8

"""
The XENCollector grabs usage/allocation metrics using libvirt

#### Dependencies
 * python-libvirt

"""

import os

from diamond.collector import Collector

try:
    import libvirt
except ImportError:
    libvirt = None


class XENCollector(Collector):
    def get_default_config_help(self):
        config_help = super(XENCollector, self).get_default_config_help()
        config_help.update({})

        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(XENCollector, self).get_default_config()
        config.update({
            'path': 'xen'
        })
        return config

    def collect(self):
        """
        Collect libvirt data
        """
        if libvirt is None:
            self.log.error('Unable to import either libvirt')
            return {}

        # Open a restricted (non-root) connection to the hypervisor
        conn = libvirt.openReadOnly(None)

        # Get hardware info
        conninfo = conn.getInfo()

        # Initialize variables
        memallocated = 0
        coresallocated = 0
        totalcores = 0
        dom_ids = conn.listDomainsID()

        if 0 in dom_ids:
            # Total cores
            dom_u = conn.lookupByID(0)
            totalcores = dom_u.info()[3]

        # Free Space
        s = os.statvfs('/')
        free_space = (s.f_bavail * s.f_frsize) / 1024

        # Calculate allocated memory and cores
        for i in dom_ids:
            # Ignore 0
            if i == 0:
                continue

            dom_u = conn.lookupByID(i)
            dominfo = dom_u.info()
            memallocated += dominfo[2]

            if i > 0:
                coresallocated += dominfo[3]

        results = {
            'InstalledMem': conninfo[1],
            'MemAllocated': memallocated / 1024,
            'MemFree': conninfo[1] - (memallocated / 1024),
            'AllocatedCores': coresallocated,
            'DiskFree': free_space,
            'TotalCores': totalcores,
            'FreeCores': (totalcores - coresallocated)
        }

        for k in results.keys():
            self.publish(k, results[k], 0)
