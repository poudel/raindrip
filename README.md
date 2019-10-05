# Introduction


## Requirements

This service relies on:

* [Apache Kafka](https://kafka.apache.org/intro)
* [PostgreSQL](https://www.postgresql.org/)
* Python 3.7


### Python requirements

Python requirements are listed in `requirements.txt`. Please install
them using pip (Preferrably inside a virutal environment.)

```shell
pip install -r requirements.txt
```

## Environment variables

Configuration options can be provided through environment variables.

The quickest way is to edit the `environ.sh` file and change the
envrionment variables to the ones that suit your setup and run:


```shell
source environ.sh
```

Note: Please make sure there is `export PYTHONPATH=.` in `environ.sh`.


## Publisher

Raindrop publisher collects various metrics about your operating
system and streams it to a Kafka queue as events. To run the publisher:

```shell
python raindrop/publisher.py
```

## Consumer

Raindrop consumer listens to the defined kafka topic and writes
incoming messages to a pre-defined PostgreSQL database in the table
`metrics`. To run the consume:


```shell
python raindrop/consumer.py
```

## Metrics

Metrics are collected by classes called metric collectors. These
classes are inside `raindrop.metrics` module at the moment.

A metric collector class should subclass
`raindrop.metrics.base.MetricCollector` class and define a class variable
`key`. The `key` should be a unique name for the metric. 

### Adding a new metric

Adding a metric is as simple as subclassing `raindrop.metrics.base.MetricCollector` like this:

```python
from raindrop.metrics.base import MetricCollector

class MyMetric(MetricCollector):
    key = "my_metric"
    
    def collect(self):
        # logic to collect metric
        return {"something": "else"}
```

The `collect` method should return a JSON serializable type.


### Present metrics

Currently there are following metrics present:

* boot_time
* number_of_processes
* number_of_users
* network_io
* battery_sensor
* virtual_memory
* swap_memory
