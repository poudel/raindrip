import json
import time
import logging
from datetime import datetime
from metrics import METRICS


logger = logging.getLogger(__name__)


def collect_metrics():
    metadata = {"machine_id": "random@hostname"}

    for metric in METRICS:
        logger.debug("Collecting %s", metric.key)

        try:
            collected_value = metric.collect()
        except Exception as err:
            logger.exception(err)
            continue

        message = {
            "key": metric.key,
            "value": collected_value,
            "now": datetime.utcnow().isoformat(),
            **metadata,
        }

        publish_message(message)


def publish_message(message):
    json_message = json.dumps(message)
    print(json_message)


if __name__ == "__main__":
    while True:
        try:
            print("Collecting...")
            collect_metrics()
            time.sleep(5)
        except KeyboardInterrupt:
            print("Exiting...")
            break
