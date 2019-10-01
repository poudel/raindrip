from importlib import import_module
from raindrop.metrics.base import MetricCollector


def get_metric_collectors(config):
    for module_name in config.metrics_modules:
        import_module(module_name)

    metrics = [
        metric_class()
        for metric_class in MetricCollector.__subclasses__()
        if metric_class.key not in config.disabled_metrics
    ]
    return metrics
