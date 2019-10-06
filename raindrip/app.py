import logging
import psycopg2
from kafka import KafkaProducer, KafkaConsumer
from raindrip.config import Config


class App:

    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger("raindrip")

        self._kafka_producer = None
        self._kafka_consumer = None
        self._pg_connection = None

    @property
    def pg_connection(self):
        if self._pg_connection:
            return self._pg_connection

        self._pg_connection = psycopg2.connect(self.config.PG_URI)
        return self._pg_connection

    @property
    def kafka_producer(self):
        if self._kafka_producer is not None:
            return self._kafka_producer

        self._kafka_producer = KafkaProducer(
            bootstrap_servers=self.config.KAFKA_URI,
            security_protocol="SSL",
            ssl_cafile=self.config.KAFKA_SSL_CAFILE,
            ssl_certfile=self.config.KAFKA_SSL_CERTFILE,
            ssl_keyfile=self.config.KAFKA_SSL_KEYFILE,
        )
        return self._kafka_producer

    @property
    def kafka_consumer(self):
        if self._kafka_consumer is not None:
            return self._kafka_consumer

        self._kafka_consumer = KafkaConsumer(
            self.config.KAFKA_TOPIC,
            auto_offset_reset="earliest",
            bootstrap_servers=self.config.KAFKA_URI,
            client_id=self.config.KAFKA_CLIENT_ID,
            group_id=self.config.KAFKA_GROUP_ID,
            security_protocol="SSL",
            ssl_cafile=self.config.KAFKA_SSL_CAFILE,
            ssl_certfile=self.config.KAFKA_SSL_CERTFILE,
            ssl_keyfile=self.config.KAFKA_SSL_KEYFILE,
        )
        return self._kafka_consumer

    def cleanup(self):
        """
        Close producer, consumer and database connections.
        """
        if self._kafka_producer:
            self._kafka_producer.close()
            self._kafka_producer = None

        if self._kafka_consumer:
            self._kafka_consumer.close()
            self._kafka_consumer = None

        if self._pg_connection:
            self._pg_connection.close()
            self._pg_connection = None


def create_app(config=None):
    config = config or Config.from_environment()
    return App(config)
