import psutil

from raindrip.metrics.base import MetricCollector


class BatterySensor(MetricCollector):
    key = "battery_sensor"

    def collect(self):
        battery = psutil.sensors_battery()
        return {
            "percent": battery.percent,
            "seconds_left": battery.secsleft,
            "power_plugged": battery.power_plugged,
        }


class VirtualMemory(MetricCollector):
    key = "virtual_memory"

    def collect(self):
        memory = psutil.virtual_memory()
        return {"total": memory.total, "available": memory.available}


class SwapMemory(MetricCollector):
    key = "swap_memory"

    def collect(self):
        swap = psutil.swap_memory()
        return {"total": swap.total, "used": swap.used, "free": swap.free}
