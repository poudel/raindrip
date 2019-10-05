import logging

from importlib import import_module
from datetime import datetime

from metrics.base import MetricCollector


logger = logging.getLogger(__name__)


def collect_metrics(metrics_modules):
    """
    Loads all metric collector classes, that is `MetricCollector`
    subclasses, and yields the metrics.
    """
    for module_name in metrics_modules:
        import_module(module_name)

    for collector_cls in MetricCollector.__subclasses__():
        try:
            collector = collector_cls()
            value = collector.collect()
        except Exception as err:
            logger.exception(err)
            continue

        yield {"key": collector.key, "value": value, "now": datetime.utcnow().isoformat()}
