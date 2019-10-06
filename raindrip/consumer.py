import json
from psycopg2.extras import execute_values


SQL_CREATE_METRICS_TABLE = """
CREATE TABLE IF NOT EXISTS metrics(
    machine_id text,
    timestamp timestamptz,
    key text,
    value jsonb
);
"""


SQL_INSERT_INTO_METRICS = """
INSERT INTO metrics(machine_id, timestamp, key, value)
VALUES %s
"""


class Consumer:

    def __init__(self, app):
        self.app = app
        self.setup()

    def setup(self):
        """
        Create the necessary PostgreSQL table where to save metrics later.
        """
        cursor = self.app.pg_connection.cursor()
        cursor.execute(SQL_CREATE_METRICS_TABLE)
        cursor.close()

        self.app.pg_connection.commit()

    def on_messages(self, messages):
        """
        This method, when called with a list of messages, does a bulk insert into the
        PostgreSQL database.
        """
        values = self._prepare_sql_values(messages)

        cursor = self.app.pg_connection.cursor()
        execute_values(cursor, SQL_INSERT_INTO_METRICS, values)
        cursor.close()

        self.app.pg_connection.commit()

    def _prepare_sql_values(self, messages):
        """
        Parse the received messages and convert them to parameters for
        the INSERT query.
        """
        parsed_messages = []
        for message in messages:
            try:
                parsed = json.loads(message.value.decode("utf-8"))
                parsed_messages.append(parsed)
            except json.JSONDecodeError:
                self.app.logger.error(
                    "Error parsing message as json: %s",
                    message.value,
                )
                continue

        values = [
            (msg["machine_id"], msg["now"], msg["key"], json.dumps(msg["value"]))
            for msg in parsed_messages
        ]
        return values

    def poll(self):
        """
        polls the kafka server for new messages
        """
        topic_messages = self.app.kafka_consumer.poll()
        for _, messages in topic_messages.items():
            self.on_messages(messages)


def consume_messages(app):
    consumer = Consumer(app)
    consumer.poll()
