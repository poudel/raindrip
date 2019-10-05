import json
from psycopg2.extras import Json, execute_values


class MessageListener:

    def __init__(self, app):
        self.app = app
        self.setup()

    def setup(self):
        """
        Create the necessary PostgreSQL table where to save metrics later.
        """
        query = """
        CREATE TABLE IF NOT EXISTS metrics(
            machine_id text,
            timestamp timestamptz,
            key text,
            value jsonb
        );
        """

        with self.app.pg_connection.cursor() as cursor:
            cursor.execute(query)

        self.app.pg_connection.commit()

    def on_messages(self, messages):
        """
        This method, when called with a list of messages, does a bulk insert into the
        PostgreSQL database.
        """
        query = "INSERT INTO metrics(machine_id, timestamp, key, value) VALUES %s"
        values = self._prepare_sql_values(messages)

        with self.app.pg_connection.cursor() as cursor:
            execute_values(cursor, query, values)

        self.app.pg_connection.commit()

    def _prepare_sql_values(self, messages):
        """
        Parse the received messages and convert them to parameters for
        the INSERT query.
        """
        parsed_messages = [json.loads(message.value.decode("utf-8")) for message in messages]

        values = [
            (msg["machine_id"], msg["now"], msg["key"], Json(msg["value"]))
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
