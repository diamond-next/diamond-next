# coding=utf-8

"""
The NvidiaGPUCollector collects GPU utilization metric using nvidia-smi.

See https://developer.nvidia.com/nvidia-system-management-interface

#### Dependencies

 * nvidia-smi
 * nvidia-ml-py (Optional)
"""

import diamond.collector

try:
    import pynvml
    USE_PYTHON_BINDING = True
except ImportError:
    USE_PYTHON_BINDING = False


class NvidiaGPUCollector(diamond.collector.ProcessCollector):
    def get_default_config_help(self):
        config_help = super(NvidiaGPUCollector, self).get_default_config_help()
        config_help.update({
            'bin': 'The path to the nvidia-smi binary',
            'stats': 'A list of Nvidia GPU stats to collect. Use `nvidia-smi --help-query-gpu` for more information'
        })

        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(NvidiaGPUCollector, self).get_default_config()
        config.update({
            'path': 'nvidia',
            'bin': '/usr/bin/nvidia-smi',
            'stats': [
                'index',
                'memory.total',
                'memory.used',
                'memory.free',
                'utilization.gpu',
                'utilization.memory',
                'temperature.gpu'
            ]
        })

        return config

    def collect_via_nvidia_smi(self, stats_config):
        """
        Use nvidia smi command line tool to collect metrics
        :param stats_config:
        :return:
        """
        raw_output = self.run_command([
            '--query-gpu={query_gpu}'.format(query_gpu=','.join(stats_config)),
            '--format=csv,nounits,noheader'
        ])

        if raw_output is None:
            return

        results = raw_output[0].strip().split("\n")

        for result in results:
            stats = result.strip().split(',')
            assert len(stats) == len(stats_config)
            index = stats[0]

            for stat_name, metric in zip(stats_config[1:], stats[1:]):
                metric_name = 'gpu_{index}.{stat_name}'.format(index=str(index), stat_name=stat_name)
                self.publish(metric_name, metric)

    def collect_via_pynvml(self, stats_config):
        """
        Use pynvml python binding to collect metrics
        :param stats_config:
        :return:
        """
        try:
            nvml_temperature_gpu = 0
            pynvml.nvmlInit()
            device_count = pynvml.nvmlDeviceGetCount()

            for device_index in range(device_count):
                handle = pynvml.nvmlDeviceGetHandleByIndex(device_index)
                memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                utilization_rates = pynvml.nvmlDeviceGetUtilizationRates(handle)

                metrics = {
                    'memory.total': memory_info.total / 1024 / 1024,
                    'memory.used': memory_info.total / 1024 / 1024,
                    'memory.free': memory_info.free / 1024 / 1024,
                    'utilization.gpu': utilization_rates.gpu,
                    'utilization.memory': utilization_rates.memory,
                    'temperature.gpu': pynvml.nvmlDeviceGetTemperature(handle, nvml_temperature_gpu)
                }

                for stat_name in stats_config[1:]:
                    metric = metrics.get(stat_name)

                    if metric:
                        metric_name = 'gpu_{index}.{stat_name}'.format(index=str(device_index), stat_name=stat_name)
                        self.publish(metric_name, metric)
        finally:
            pynvml.nvmlShutdown()

    def collect(self):
        """
        Collector GPU stats
        """
        stats_config = self.config['stats']

        if USE_PYTHON_BINDING:
            collect_metrics = self.collect_via_pynvml
        else:
            collect_metrics = self.collect_via_nvidia_smi

        collect_metrics(stats_config)
