import logging

from importlib import import_module
from datetime import datetime

from raindrop.metrics.base import MetricCollector


logger = logging.getLogger(__name__)


def collect_metrics(metrics_modules):
    for module_name in metrics_modules:
        import_module(module_name)

    collectors = [collector() for collector in MetricCollector.__subclasses__()]

    for collector in collectors:
        try:
            value = collector.collect()
        except Exception as err:
            logger.exception(err)
            continue

        yield {"key": collector.key, "value": value, "now": datetime.now().isoformat()}
