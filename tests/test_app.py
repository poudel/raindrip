from unittest import TestCase, mock
from raindrip.app import App


class TestApp(TestCase):

    def setUp(self):
        self.fake_config = mock.MagicMock(LOGLEVEL="INFO")

    @mock.patch("raindrip.app.logging")
    def test__init__(self, logging_mock):
        config = mock.MagicMock(LOGLEVEL="INFOX")
        app = App(config)

        logging_mock.basicConfig.assert_called_once_with(level="INFOX")

        self.assertIsNotNone(app.logger)
        self.assertIsNotNone(app.config)

        self.assertIsNone(app._kafka_consumer)
        self.assertIsNone(app._kafka_producer)
        self.assertIsNone(app._pg_connection)

    @mock.patch("raindrip.app.psycopg2")
    def test_pg_connection(self, psycopg2_mock):
        app = App(self.fake_config)

        connection = app.pg_connection

        self.assertIsNotNone(app._pg_connection)
        self.assertEqual(connection, app._pg_connection)
        psycopg2_mock.connect.assert_called_once_with(self.fake_config.PG_URI)

    @mock.patch("raindrip.app.KafkaProducer")
    def test_kafka_producer(self, producer_mock):
        app = App(self.fake_config)
        producer = app.kafka_producer

        self.assertIsNotNone(app._kafka_producer)
        self.assertEqual(producer, app._kafka_producer)

        producer_mock.assert_called_once_with(
            bootstrap_servers=self.fake_config.KAFKA_URI,
            security_protocol="SSL",
            ssl_cafile=self.fake_config.KAFKA_SSL_CAFILE,
            ssl_certfile=self.fake_config.KAFKA_SSL_CERTFILE,
            ssl_keyfile=self.fake_config.KAFKA_SSL_KEYFILE,
        )

    @mock.patch("raindrip.app.KafkaConsumer")
    def test_kafka_consumer(self, consumer_mock):
        app = App(self.fake_config)
        consumer = app.kafka_consumer

        self.assertIsNotNone(app._kafka_consumer)
        self.assertEqual(consumer, app._kafka_consumer)

        consumer_mock.assert_called_once_with(
            self.fake_config.KAFKA_TOPIC,
            auto_offset_reset="earliest",
            bootstrap_servers=self.fake_config.KAFKA_URI,
            client_id=self.fake_config.KAFKA_CLIENT_ID,
            group_id=self.fake_config.KAFKA_GROUP_ID,
            security_protocol="SSL",
            ssl_cafile=self.fake_config.KAFKA_SSL_CAFILE,
            ssl_certfile=self.fake_config.KAFKA_SSL_CERTFILE,
            ssl_keyfile=self.fake_config.KAFKA_SSL_KEYFILE,
        )

    def test_cleanup(self):
        app = mock.MagicMock()
        kafka_producer = app._kafka_producer
        kafka_consumer = app._kafka_consumer
        pg_connection = app._pg_connection

        App.cleanup(app)

        kafka_producer.close.assert_called_once()
        kafka_consumer.close.assert_called_once()
        pg_connection.close.assert_called_once()

        self.assertIsNone(app._kafka_producer)
        self.assertIsNone(app._kafka_consumer)
        self.assertIsNone(app._pg_connection)
