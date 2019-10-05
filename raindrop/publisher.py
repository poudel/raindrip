import json
import time

from raindrop.config import config
from raindrop.app import App
from raindrop.metrics import collect_metrics


def publish_metrics(app):
    for metric_value in collect_metrics(app.config.METRICS_MODULES):
        message = {"machine_id": app.config.MACHINE_ID, **metric_value}
        json_message = json.dumps(message)
        app.kafka_producer.send(app.config.KAFKA_TOPIC, json_message.encode("utf-8"))

    app.kafka_producer.flush()


def publish_messages(app):
    while True:
        try:
            app.logger.info("Publishing...")
            publish_metrics(app)
            time.sleep(5)
        except KeyboardInterrupt:
            app.logger.info("Exiting raindrop publisher...")
            break


if __name__ == "__main__":
    app = App(config)
    publish_messages(app)
