import json
from unittest import TestCase, mock
from raindrip.consumer import Consumer, SQL_CREATE_METRICS_TABLE, SQL_INSERT_INTO_METRICS


class ConsumerTest(TestCase):
    def test__init__(self):
        app = mock.MagicMock()
        consumer = Consumer(app)

        self.assertEqual(consumer.app, app)

        cursor = app.pg_connection.cursor.return_value
        cursor.execute.assert_called_once_with(SQL_CREATE_METRICS_TABLE)
        cursor.close.assert_called_once()

        app.pg_connection.commit.assert_called_once()

    @mock.patch("raindrip.consumer.execute_values")
    def test_on_messages(self, execute_values_mock):
        app = mock.MagicMock()
        consumer = Consumer(app)

        message = {
            "machine_id": "asdf",
            "now": "2018-01-01 01:01:01",
            "key": "battery_sensor",
            "value": {"something": "else"},
        }
        encoded_msg = json.dumps(message).encode("utf-8")
        messages = [mock.MagicMock(value=encoded_msg)]
        values = consumer._prepare_sql_values(messages)

        consumer.on_messages(messages)

        cursor = app.pg_connection.cursor.return_value
        execute_values_mock.assert_called_once_with(cursor, SQL_INSERT_INTO_METRICS, values)

    def test__prepare_sql_values(self):
        app = mock.MagicMock()
        consumer = Consumer(app)

        message = {
            "machine_id": "asdf",
            "now": "2018-01-01 01:01:01",
            "key": "battery_sensor",
            "value": {"something": "else"},
        }
        encoded_msg = json.dumps(message).encode("utf-8")
        messages = [mock.MagicMock(value=encoded_msg)]

        expected_values = [
            (message["machine_id"], message["now"], message["key"], json.dumps(message["value"]))
        ]

        values = consumer._prepare_sql_values(messages)

        self.assertEqual(values, expected_values)

    def test__prepare_sql_values_ignores_encoding_error(self):
        app = mock.MagicMock()
        consumer = Consumer(app)

        messages = [mock.MagicMock(value=b'{')]
        values = consumer._prepare_sql_values(messages)

        self.assertEqual(values, [])
