import json
import time
import logging
from kafka import KafkaProducer

from raindrop.config import config
from raindrop.metrics import collect_metrics


logger = logging.getLogger(__name__)


producer = KafkaProducer(
    bootstrap_servers=config.kafka_uri,
    security_protocol="SSL",
    ssl_cafile=config.kafka_ssl_ca_file,
    ssl_certfile=config.kafka_ssl_cert_file,
    ssl_keyfile=config.kafka_ssl_key_file,
)


def publish_metrics():
    for metric_value in collect_metrics(config):
        message = {"machine_id": config.machine_id, **metric_value}
        json_message = json.dumps(message)
        producer.send(config.kafka_topic, json_message.encode("utf-8"))

    producer.flush()


if __name__ == "__main__":

    while True:
        try:
            print("Collecting...")
            publish_metrics()
            time.sleep(5)
        except KeyboardInterrupt:
            print("Exiting...")
            break
