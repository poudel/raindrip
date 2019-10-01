import psutil

from metrics.base import BaseMetric


class BatterySensor(BaseMetric):
    key = "battery_sensor"

    def collect(self):
        battery = psutil.sensors_battery()
        return {
            "percent": battery.percent,
            "seconds_left": battery.secsleft,
            "power_plugged": battery.power_plugged,
        }


class VirtualMemory(BaseMetric):
    key = "virtual_memory"

    def collect(self):
        memory = psutil.virtual_memory()
        return {"total": memory.total, "available": memory.available}


class SwapMemory(BaseMetric):
    key = "swap_memory"

    def collect(self):
        swap = psutil.swap_memory()
        return {"total": swap.total, "used": swap.used, "free": swap.free}


METRICS = [BatterySensor(), VirtualMemory(), SwapMemory()]
