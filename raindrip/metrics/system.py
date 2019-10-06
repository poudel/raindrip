from datetime import datetime

import psutil

from raindrip.metrics.base import MetricCollector


class BootTime(MetricCollector):
    key = "boot_time"

    def collect(self):
        boot_time = datetime.fromtimestamp(psutil.boot_time())

        # needs to be .now() because we're comparing local time
        uptime = (datetime.now() - boot_time).total_seconds()
        return {"when": boot_time.isoformat(), "uptime": uptime}


class NumProcesses(MetricCollector):
    key = "number_of_processes"

    def collect(self):
        return len(psutil.pids())


class NumUsers(MetricCollector):
    key = "number_of_users"

    def collect(self):
        return len(psutil.users())
