# Raindrip

## Requirements

This app relies on following:

* [Apache Kafka](https://kafka.apache.org/intro)
* [PostgreSQL](https://www.postgresql.org/)
* Python 3.7


## Installation

The easiest way would be to install it from PyPi. Activate a
virutalenv and run this:

```shell
pip install raindrip
```

For local development and testing, you may want to skip to the last
section.

## Configuration

Raindrip needs to be configured through environment variables before
it can be used. The following variables are required. Please set the
values and export them before running the commands.


```shell
export RAIN_KAFKA_URI=
export RAIN_KAFKA_SSL_CAFILE=/path/to/ca.pem
export RAIN_KAFKA_SSL_CERTFILE=/path/to/service.cert
export RAIN_KAFKA_SSL_KEYFILE=/path/to/service.key

# the topic you want to broadcast to
export RAIN_KAFKA_TOPIC=raindrip

export RAIN_PG_URI=postgres://user:password@host:port/db?sslmode=required
```


## The Publisher

Raindrip publisher collects various metrics about your operating
system and streams it to the specified Kafka topic. To run the
publisher:

```shell
raindrip publisher
```

## The Consumer

Raindrip consumer listens to the defined kafka topic and writes
incoming messages to a pre-defined PostgreSQL database in the table
`metrics`. To run the consume:


```shell
raindrip consumer
```

Once the consumer starts running, it will decode all incoming metrics
and save them in the database you specified through `RAIN_PG_URI` in a table called `metrics`.

Connect to the PostgreSQL shell.

```shell
psql postgres://user:password@host:port/db?sslmode=required
```

Run the following queries, for example:

Get number of entries

```sql
SELECT count(*) FROM metrics;
```

or get number of entries for each metrics

```sql
SELECT DISTINCT key, COUNT(*) FROM metrics GROUP BY key;
```

and so on.

# Local development

Clone the repository and go inside the `raindrip` directory.

```shell
git clone git@github.com:poudel/raindrip.git
```

Along with the requirements listed in the section above, this project
relies on [`poetry`](https://poetry.eustace.io/docs/) to manage
dependencies.

Install `poetry` by running:

```shell
pip install --user poetry
```

Once you have it installed, run the following to install the dependencies.

```shell
poetry install
```

Poetry will create a new virtual environment and install the
dependencies there. Any command that you need to run should be run like this:

```shell
poetry run <command> arg1...argN
```

## Configuration

Configuration, again, are done via environment variables. Read the
section above.


## Tests

Tests are inside `tests/` directory. They can be run using python's
default test runner.


```shell
poetry run python -m unittest
```


## Adding metrics

Metrics are collected by classes called metric collectors. These
classes are inside `raindrip.metrics` module at the moment.

A metric collector class should subclass
`raindrip.metrics.base.MetricCollector` class and define a class
variable `key`. The `key` should be a unique name for the metric.


### Adding a new metric

Adding a metric is as simple as subclassing `raindrip.metrics.base.MetricCollector` like this:

```python
from raindrip.metrics.base import MetricCollector

class MyMetric(MetricCollector):
    key = "my_metric"
    
    def collect(self):
        # logic to collect metric
        return {"something": "else"}
```

The `collect` method should return a JSON serializable type.

Now the module with your metrics needs to be registered in
`config.py`. Open `config.py` and add the full path of your metric
module in `Config.METRICS_MODULES` list.


### Built-in metrics

Currently there are following metrics present:

* boot_time
* number_of_processes
* number_of_users
* network_io
* battery_sensor
* virtual_memory
* swap_memory
