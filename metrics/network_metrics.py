import psutil
from metrics.base import BaseMetric


class NetworkIO(BaseMetric):
    key = "network_io"

    def collect(self):
        counter = psutil.net_io_counters()
        return {'bytes_sent': counter.bytes_sent, 'bytes_received': counter.bytes_recv}


METRICS = [NetworkIO()]
