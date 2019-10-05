import os


def env(name, default=None):
    """
    This function makes sure that we don't load the config unless all
    required environment variables are provided.
    """
    value = os.environ.get(name)

    if value is None and default is None:
        raise RuntimeError(f"Environment variable '{name}' must be provided.")

    return value or default


class Config:
    METRICS_MODULES = ["metrics.hardware", "metrics.network", "metrics.system"]

    MACHINE_ID = env("RAIN_MACHINE_ID", "random@machine")
    LOGLEVEL = env("RAIN_LOGLEVEL", "INFO").upper()

    KAFKA_URI = env("RAIN_KAFKA_URI")
    KAFKA_SSL_CAFILE = env("RAIN_KAFKA_SSL_CAFILE")
    KAFKA_SSL_CERTFILE = env("RAIN_KAFKA_SSL_CERTFILE")
    KAFKA_SSL_KEYFILE = env("RAIN_KAFKA_SSL_KEYFILE")

    KAFKA_TOPIC = env("RAIN_KAFKA_TOPIC")
    KAFKA_CLIENT_ID = env("RAIN_KAFKA_CLIENT_ID", "raindrop-client")
    KAFKA_GROUP_ID = env("RAIN_KAFKA_GROUP_ID", "raindrop-group")

    PG_URI = env("RAIN_PG_URI")


config = Config()
