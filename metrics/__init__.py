from metrics import hardware_metrics, network_metrics, system_metrics


METRICS = []
METRICS += hardware_metrics.METRICS
METRICS += network_metrics.METRICS
METRICS += system_metrics.METRICS
