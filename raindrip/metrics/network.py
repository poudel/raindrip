import psutil
from raindrip.metrics.base import MetricCollector


class NetworkIO(MetricCollector):
    key = "network_io"

    def collect(self):
        counter = psutil.net_io_counters()
        return {"bytes_sent": counter.bytes_sent, "bytes_received": counter.bytes_recv}
