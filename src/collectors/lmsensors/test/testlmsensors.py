#!/usr/bin/python3
# coding=utf-8

import unittest
from unittest.mock import patch

from collectors.lmsensors.lmsensors import LMSensorsCollector
from diamond.collector import Collector
from diamond.testing import CollectorTestCase
from test import get_collector_config

try:
    import sensors

    sensors
except ImportError:
    sensors = None


class FeatureMock:
    def __init__(self, label, value=None):
        self.label = label
        self.value = value

    def get_value(self):
        if self.value is not None:
            return self.value

        raise Exception("Value not present")


class ChipMock:
    def __init__(self, label, features):
        self.label = label
        self.features = features

    def __iter__(self):
        for feature in self.features:
            yield feature

    def __str__(self):
        return self.label


@unittest.skipIf(sensors is None, "No PySensors module found")
class TestLMSensorsCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config("LMSensorsCollector", {})
        self.collector = LMSensorsCollector(config, None)

    def test_import(self):
        self.assertTrue(LMSensorsCollector)

    @patch.object(Collector, "publish")
    def test_simple_sensor(self, publish_mock):
        feature = FeatureMock("Core 0", 10)
        chip = ChipMock("coretemp-isa-0000", [feature])
        patch_detected_chips_iter = patch(
            "sensors.iter_detected_chips", return_value=[chip]
        )
        patch_detected_chips_iter.start()
        self.collector.collect()
        patch_detected_chips_iter.stop()
        self.assertPublished(publish_mock, "coretemp-isa-0000.Core-0", 10)

    @patch.object(Collector, "publish")
    def test_empty_sensor(self, publish_mock):
        feature = FeatureMock("Core 0")
        chip = ChipMock("coretemp-isa-0000", [feature])
        patch_detected_chips_iter = patch(
            "sensors.iter_detected_chips", return_value=[chip]
        )
        patch_detected_chips_iter.start()
        self.collector.collect()
        patch_detected_chips_iter.stop()
        self.assertUnpublished(publish_mock, "coretemp-isa-0000.Core-0", None)

    @patch.object(Collector, "publish")
    def test_empty_zero_sensor(self, publish_mock):
        self.collector.config["send_zero"] = True

        feature = FeatureMock("Core 0")
        chip = ChipMock("coretemp-isa-0000", [feature])
        patch_detected_chips_iter = patch(
            "sensors.iter_detected_chips", return_value=[chip]
        )
        patch_detected_chips_iter.start()
        self.collector.collect()
        patch_detected_chips_iter.stop()
        self.assertPublished(publish_mock, "coretemp-isa-0000.Core-0", 0)
