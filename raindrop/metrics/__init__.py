import logging

from importlib import import_module
from datetime import datetime

from raindrop.metrics.base import MetricCollector


logger = logging.getLogger(__name__)


def get_metric_collectors(config):
    for module_name in config.METRICS_MODULES:
        import_module(module_name)

    return [collector() for collector in MetricCollector.__subclasses__()]


def collect_metrics(config):
    collectors = get_metric_collectors(config)

    for collector in collectors:
        try:
            value = collector.collect()
        except Exception as err:
            logger.exception(err)
            continue

        yield {"key": collector.key, "value": value, "now": datetime.now().isoformat()}
