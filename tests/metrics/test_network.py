from unittest import TestCase
from raindrop.metrics.network import NetworkIO


class TestNetworkMetrics(TestCase):

    def test_NetworkIO(self):
        metric = NetworkIO()
        value = metric.collect()

        self.assertEqual(metric.key, "network_io")
        self.assertIsInstance(value, dict)
        self.assertIsInstance(value["bytes_sent"], int)
        self.assertIsInstance(value["bytes_received"], int)
