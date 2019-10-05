import os


def env(name, default=None):
    value = os.environ.get(name)

    if value is None and default is None:
        raise RuntimeError(f"Environment variable '{name}' must be provided.")

    return value or default


class BaseConfig:
    metrics_modules = ["metrics.hardware", "metrics.network", "metrics.system"]

    machine_id = env("RAIN_MACHINE_ID", "random@machine")

    kafka_uri = env("RAIN_KAFKA_URI")
    kafka_ssl_ca_file = env("RAIN_KAFKA_SSL_CA_FILE")
    kafka_ssl_cert_file = env("RAIN_KAFKA_SSL_CERT_FILE")
    kafka_ssl_key_file = env("RAIN_KAFKA_SSL_KEY_FILE")
    kafka_topic = env("RAIN_KAFKA_TOPIC")


config = BaseConfig()
