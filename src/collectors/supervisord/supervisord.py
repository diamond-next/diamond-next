# coding=utf-8

"""
Custom collector for supervisord process control system
(github.com/Supervisor/supervisor)

Supervisor runs an XML-RPC server, which this collector uses to gather a few
basic stats on each registered process.

#### Dependencies

 * xmlrpc
 * supervisor
 * diamond

#### Usage

Configure supervisor's XML-RPC server (either over HTTP or Unix socket). See
supervisord.org/configuration.html for details. In the collector configuration
file, you may specify the protocol and path configuration; below are the
defaults.

<pre>
xmlrpc_server_protocol = unix
xmlrpc_server_path = /var/run/supervisor.sock
</pre>

"""

import xmlrpc.client

import diamond.collector

try:
    import supervisor.xmlrpc
except ImportError:
    supervisor = None


class SupervisordCollector(diamond.collector.Collector):
    def get_default_config_help(self):
        config_help = super(SupervisordCollector, self).get_default_config_help()
        config_help.update(
            {
                "xmlrpc_server_protocol": "XML-RPC server protocol. Options: unix, http",  # NOQA
                "xmlrpc_server_path": "XML-RPC server path.",
            }
        )
        return config_help

    def get_default_config(self):
        default_config = super(SupervisordCollector, self).get_default_config()
        default_config["path"] = "supervisor"
        default_config["xmlrpc_server_protocol"] = "unix"
        default_config["xmlrpc_server_path"] = "/var/run/supervisor.sock"

        return default_config

    def get_all_process_info(self):
        server = None
        protocol = self.config["xmlrpc_server_protocol"]
        path = self.config["xmlrpc_server_path"]
        uri = "{}://{}".format(protocol, path)

        self.log.debug('Attempting to connect to XML-RPC server "%s"', uri)

        if protocol == "unix":
            server = xmlrpc.client.ServerProxy(
                "http://127.0.0.1",
                supervisor.xmlrpc.SupervisorTransport(None, None, uri),
            ).supervisor
        elif protocol == "http":
            server = xmlrpc.client.Server(uri).supervisor
        else:
            self.log.debug(
                'Invalid xmlrpc_server_protocol config setting "%s"', protocol
            )

            return None

        return server.get_all_process_info()

    def collect(self):
        processes = self.get_all_process_info()

        self.log.debug("Found %s supervisord processes", len(processes))

        for process in processes:
            stat_prefix = "%s.%s" % (process["group"], process["name"])

            # state

            self.publish(stat_prefix + ".state", process["state"])

            # uptime

            uptime = 0

            if process["statename"] == "RUNNING":
                uptime = process["now"] - process["start"]

            self.publish(stat_prefix + ".uptime", uptime)
