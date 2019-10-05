import json
import time
import logging

from raindrop.config import config
from raindrop.metrics import collect_metrics
from raindrop.kafka_utils import kafka


logger = logging.getLogger(__name__)


def publish_metrics(producer):
    for metric_value in collect_metrics(config):
        message = {"machine_id": config.MACHINE_ID, **metric_value}
        json_message = json.dumps(message)
        producer.send(config.KAFKA_TOPIC, json_message.encode("utf-8"))

    producer.flush()


def publish_messages():
    while True:
        try:
            print("Collecting...")
            publish_metrics(config, kafka.producer)
            time.sleep(5)
        except KeyboardInterrupt:
            print("Exiting raindrop publisher...")
            break
