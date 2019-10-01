from unittest import TestCase
from raindrop.metrics.system import BootTime, NumProcesses, NumUsers


class TestSystemMetrics(TestCase):
    def test_BootTime(self):
        metric = BootTime()
        value = metric.collect()

        self.assertEqual(metric.key, "boot_time")
        self.assertIsInstance(value, dict)
        self.assertIsInstance(value["when"], str)
        self.assertIsInstance(value["uptime"], float)

    def test_NumProcesses(self):
        metric = NumProcesses()
        value = metric.collect()

        self.assertEqual(metric.key, "number_of_processes")
        self.assertIsInstance(value, int)

    def test_NumUsers(self):
        metric = NumUsers()
        value = metric.collect()

        self.assertEqual(metric.key, "number_of_users")
        self.assertIsInstance(value, int)
