import json
import time
import logging
from datetime import datetime

from raindrop.config import config
from raindrop.metrics import get_metric_collectors


logger = logging.getLogger(__name__)


def collect_metrics():
    metadata = {"machine_id": "random@hostname"}

    collectors = get_metric_collectors(config)

    for collector in collectors:
        logger.debug("Collecting %s", collector.key)

        try:
            collected_value = collector.collect()
        except Exception as err:
            logger.exception(err)
            continue

        message = {
            "key": collector.key,
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
