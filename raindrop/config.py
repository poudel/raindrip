class BaseConfig:
    metrics_modules = [
        "metrics.hardware",
        "metrics.network",
        "metrics.system",
    ]
    disabled_metrics = [
        "battery_sensor",
    ]

    kafka_uri = None


config = BaseConfig()
