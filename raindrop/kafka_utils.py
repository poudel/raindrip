from kafka import KafkaProducer, KafkaConsumer
from raindrop.config import config


class KafkaProxy:
    def __init__(self, config):
        self.config = config
        self._producer = None
        self._consumer = None

    @property
    def producer(self):
        if self._producer is not None:
            return self._producer

        self._producer = KafkaProducer(
            bootstrap_servers=self.config.KAFKA_URI,
            security_protocol="SSL",
            ssl_cafile=self.config.KAFKA_SSL_CAFILE,
            ssl_certfile=self.config.KAFKA_SSL_CERTFILE,
            ssl_keyfile=self.config.KAFKA_SSL_KEYFILE,
        )
        return self._producer

    @property
    def consumer(self):
        if self._consumer is not None:
            return self._consumer

        self._consumer = KafkaConsumer(
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
        return self._consumer


kafka = KafkaProxy(config)
