# coding=utf-8

"""
Collect statistics from Mogilefs

#### Dependencies

 * socket
 * time
"""

import socket
import time

import diamond.collector


class _TelnetSocket:
    """
    Minimal socket wrapper providing the telnet-like interface used by
    MogilefsCollector (replaces the removed telnetlib.Telnet).
    """

    def __init__(self, host, port, timeout=None):
        self._sock = socket.create_connection((host, port), timeout=timeout)
        self._buf = b""

    def write(self, data):
        if isinstance(data, str):
            data = data.encode("ascii")
        self._sock.sendall(data)

    def read_until(self, terminator, timeout=None):
        if isinstance(terminator, str):
            terminator = terminator.encode("ascii")
        if timeout is not None:
            self._sock.settimeout(timeout)
        try:
            while terminator not in self._buf:
                chunk = self._sock.recv(4096)
                if not chunk:
                    break
                self._buf += chunk
        except socket.timeout:
            pass
        idx = self._buf.find(terminator)
        if idx >= 0:
            result = self._buf[: idx + len(terminator)]
            self._buf = self._buf[idx + len(terminator) :]
        else:
            result = self._buf
            self._buf = b""
        return result.decode("ascii", errors="replace")

    def close(self):
        self._sock.close()


class MogilefsCollector(diamond.collector.Collector):
    def get_default_config_help(self):
        config_help = super(MogilefsCollector, self).get_default_config_help()
        config_help.update(
            {
                "path": "Metric path",
            }
        )

        return config_help

    def get_default_config(self):
        config = super(MogilefsCollector, self).get_default_config()
        config.update({"path": "mogilefs"})

        return config

    def collect(self):
        tn = _TelnetSocket("127.0.0.1", 7001, timeout=3)
        time.sleep(1)
        tn.write("!stats\r\n")
        out = tn.read_until(".", 3)
        tn.close()

        myvars = {}

        for line in out.splitlines()[:-1]:
            name, var = line.partition(" ")[::2]
            myvars[name.strip()] = int(var)

        for key, value in iter(myvars.items()):
            # Set Metric Name
            metric_name = key

            # Set Metric Value
            metric_value = value

            # Publish Metric
            self.publish(metric_name, metric_value)
