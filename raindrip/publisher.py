import json

from raindrip.metrics import collect_metrics


def publish_messages(app):
    for metric_value in collect_metrics(app.config.METRICS_MODULES):
        message = {"machine_id": app.config.MACHINE_ID, **metric_value}
        json_message = json.dumps(message)
        app.kafka_producer.send(app.config.KAFKA_TOPIC, json_message.encode("utf-8"))

    app.kafka_producer.flush()
