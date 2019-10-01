from unittest import TestCase
from raindrop.metrics.hardware import BatterySensor, VirtualMemory, SwapMemory


class TestHardwareMetrics(TestCase):

    def test_BatterySensor(self):
        metric = BatterySensor()
        value = metric.collect()

        self.assertEqual(metric.key, "battery_sensor")
        self.assertIsInstance(value, dict)

        self.assertIsInstance(value["percent"], float)
        self.assertIsInstance(value["seconds_left"], int)
        self.assertIsInstance(value["power_plugged"], bool)

    def test_VirtualMemory(self):
        metric = VirtualMemory()
        value = metric.collect()

        self.assertEqual(metric.key, "virtual_memory")
        self.assertIsInstance(value, dict)

        self.assertIsInstance(value["total"], int)
        self.assertIsInstance(value["available"], int)

    def test_SwapMemory(self):
        metric = SwapMemory()
        value = metric.collect()

        self.assertEqual(metric.key, "swap_memory")
        self.assertIsInstance(value, dict)

        self.assertIsInstance(value["total"], int)
        self.assertIsInstance(value["used"], int)
        self.assertIsInstance(value["free"], int)
