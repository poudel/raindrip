# Introduction


## Requirements

This service relies on:

* [Apache Kafka](https://kafka.apache.org/intro)
* [PostgreSQL](https://www.postgresql.org/)
* Python 3.7

### Python requirements

Python requirements are listed in `requirements.txt`. Please install them using pip.

```shell
pip install -r requirements.txt
```


## Configuration

Configuration options can be provided through environment variables.

The quickest way is to edit the `environ.sh` file and change the
envrionment variables to the ones that suit your setup and run:


```shell
source environ.sh
```


## Publisher

Raindrop publisher collects various metrics about your operating
system and streams it to a Kafka queue as events.

## Consumer

Raindrop consumer can listen to a Kafka queue and then consume events
as defined.
