from unittest import TestCase, mock
from raindrip.config import Config
from raindrip.exceptions import ConfigMissing


class TestConfig(TestCase):
    @mock.patch("raindrip.config.os")
    def test_from_environment(self, os_mock):
        os_mock.environ = {
            "RAIN_MACHINE_ID": "machine-id",
            "RAIN_KAFKA_URI": "kafka-uri",
            "RAIN_KAFKA_SSL_CAFILE": "some.pem",
            "RAIN_KAFKA_SSL_CERTFILE": "cert.txt",
            "RAIN_KAFKA_SSL_KEYFILE": "key.txt",
            "RAIN_KAFKA_TOPIC": "rainbow",
            "RAIN_KAFKA_CLIENT_ID": "client-id",
            "RAIN_KAFKA_GROUP_ID": "group-id",
            "RAIN_PG_URI": "pg-uri",
        }

        config = Config.from_environment()

        self.assertEqual(config.MACHINE_ID, "machine-id")
        self.assertEqual(config.KAFKA_URI, "kafka-uri")
        self.assertEqual(config.KAFKA_SSL_CAFILE, "some.pem")
        self.assertEqual(config.KAFKA_SSL_CERTFILE, "cert.txt")
        self.assertEqual(config.KAFKA_SSL_KEYFILE, "key.txt")
        self.assertEqual(config.KAFKA_TOPIC, "rainbow")
        self.assertEqual(config.KAFKA_CLIENT_ID, "client-id")
        self.assertEqual(config.KAFKA_GROUP_ID, "group-id")
        self.assertEqual(config.PG_URI, "pg-uri")

        self.assertEqual(
            config.METRICS_MODULES,
            ["raindrip.metrics.hardware", "raindrip.metrics.network", "raindrip.metrics.system"],
        )

    def test_from_environment_raises_for_missing_env_vars(self):
        with self.assertRaises(ConfigMissing) as cm:
            Config.from_environment()

        self.assertEqual(
            cm.exception.missing,
            [
                'RAIN_KAFKA_URI',
                'RAIN_KAFKA_SSL_CAFILE',
                'RAIN_KAFKA_SSL_CERTFILE',
                'RAIN_KAFKA_SSL_KEYFILE',
                'RAIN_KAFKA_TOPIC',
                'RAIN_PG_URI',
            ],
        )
