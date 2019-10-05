import json
import psycopg2
from psycopg2.extras import Json, execute_values
from raindrop.kafka_utils import kafka


class MessageHandler:
    def __init__(self, config):
        self.config = config
        self._connection = None

    @property
    def connection(self):
        if self._connection:
            return self._connection

        self._connection = psycopg2.connect(self.config.PG_URI)
        return self._connection

    def before(self):
        query = """
        CREATE TABLE IF NOT EXISTS metrics(
            machine_id text,
            timestamp timestamptz,
            key text,
            value jsonb
        );
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query)

        self.connection.commit()

    def after(self):
        if self._connection:
            self._connection.close()
            self._connection = None

    def on_messages(self, messages):
        query = "INSERT INTO metrics(machine_id, timestamp, key, value) VALUES %s"
        values = self._prepare_sql_values(messages)

        with self.connection.cursor() as cursor:
            execute_values(cursor, query, values)

        self.connection.commit()

    def _prepare_sql_values(self, messages):
        parsed_messages = [json.loads(message.value.decode("utf-8")) for message in messages]

        values = [
            (msg["machine_id"], msg["now"], msg["key"], Json(msg["value"]))
            for msg in parsed_messages
        ]
        return values

    def poll(self):
        topic_messages = kafka.consumer.poll(timeout_ms=1000)
        for _, messages in topic_messages.items():
            self.on_messages(messages)
