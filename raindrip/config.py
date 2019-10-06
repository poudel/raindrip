import os
from dataclasses import dataclass, fields


@dataclass
class Config:
    METRICS_MODULES = [
        "raindrip.metrics.hardware",
        "raindrip.metrics.network",
        "raindrip.metrics.system",
    ]

    LOGLEVEL: str
    MACHINE_ID: str

    KAFKA_URI: str
    KAFKA_SSL_CAFILE: str
    KAFKA_SSL_CERTFILE: str
    KAFKA_SSL_KEYFILE: str

    KAFKA_TOPIC: str
    KAFKA_CLIENT_ID: str
    KAFKA_GROUP_ID: str

    PG_URI: str

    @classmethod
    def from_environment(cls, env_var_prefix="RAIN"):
        defaults = {
            "MACHINE_ID": "random@machine",
            "LOGLEVEL": "INFO",
            "KAFKA_CLIENT_ID": "raindrip-client",
            "KAFKA_GROUP_ID": "raindrip-group",
        }
        values = {}

        for field in fields(cls):
            default = defaults.get(field.name)

            env_var_name = f"{env_var_prefix}_{field.name}"
            value = os.environ.get(env_var_name, default)

            if value is None:
                raise RuntimeError(f"Environment variable '{env_var_name}' must be provided.")

            values[field.name] = value
        return cls(**values)
