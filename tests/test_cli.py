from unittest import TestCase, mock
from raindrip.cli import main


class TestCli(TestCase):
    @mock.patch("raindrip.cli.time")
    @mock.patch("raindrip.cli.parse_args")
    def test_main_with_invalid_command(self, parse_args_mock, time_mock):
        parse_args_mock.return_value = mock.MagicMock(command="random1", loglevel="INFO")

        with self.assertLogs(level="ERROR") as cm:
            exit_code = main()

        self.assertEqual(exit_code, 1)
        self.assertRegex(cm.output[0], r"ERROR:raindrip:Unknown command: random1")

    @mock.patch("raindrip.cli.time")
    @mock.patch("raindrip.cli.parse_args")
    def test_main_without_env_variables(self, parse_args_mock, time_mock):
        parse_args_mock.return_value = mock.MagicMock(command="consumer", loglevel="INFO")

        with self.assertLogs("raindrip", level="ERROR") as cm:
            exit_code = main()

        self.assertEqual(exit_code, 1)
        self.assertRegex(cm.output[0], r"ERROR:raindrip:Failed to start. ")

    @mock.patch("raindrip.cli.time")
    @mock.patch("raindrip.cli.parse_args")
    @mock.patch("raindrip.cli.create_app")
    @mock.patch("raindrip.cli.consume_messages")
    def test_main_consumer(self, consume_messages, create_app_mock, parse_args_mock, time_mock):
        fake_app = create_app_mock.return_value

        args = mock.MagicMock(command="consumer", loglevel="INFO")
        parse_args_mock.return_value = args

        # to break the loop
        consume_messages.side_effect = KeyboardInterrupt()

        with self.assertLogs("raindrip", level="INFO") as cm:
            exit_code = main()

        self.assertEqual(
            cm.output,
            [
                "INFO:raindrip:Starting consumer",
                "INFO:raindrip:Gracefully stopping consumer",
                "INFO:raindrip:Cleaning up..",
            ],
        )

        self.assertEqual(exit_code, 0)
        consume_messages.assert_called_once_with(fake_app)
        fake_app.cleanup.assert_called_once()

    @mock.patch("raindrip.cli.time")
    @mock.patch("raindrip.cli.parse_args")
    @mock.patch("raindrip.cli.create_app")
    @mock.patch("raindrip.cli.publish_messages")
    def test_main_publisher(self, publish_messages, create_app_mock, parse_args_mock, time_mock):
        fake_app = create_app_mock.return_value

        args = mock.MagicMock(command="publisher", loglevel="INFO")
        parse_args_mock.return_value = args

        # to break the loop
        publish_messages.side_effect = KeyboardInterrupt()

        with self.assertLogs("raindrip", level="INFO") as cm:
            exit_code = main()

        self.assertEqual(
            cm.output,
            [
                "INFO:raindrip:Starting publisher",
                "INFO:raindrip:Gracefully stopping publisher",
                "INFO:raindrip:Cleaning up..",
            ],
        )

        self.assertEqual(exit_code, 0)
        publish_messages.assert_called_once_with(fake_app)
        fake_app.cleanup.assert_called_once()

    @mock.patch("raindrip.cli.time")
    @mock.patch("raindrip.cli.parse_args")
    @mock.patch("raindrip.cli.create_app")
    @mock.patch("raindrip.cli.publish_messages")
    def test_main_time_sleep(self, publish_messages, create_app_mock, parse_args_mock, time_mock):
        fake_app = create_app_mock.return_value

        args = mock.MagicMock(command="publisher", loglevel="INFO", frequency=1)
        parse_args_mock.return_value = args

        # to break the loop
        time_mock.sleep.side_effect = KeyboardInterrupt()

        exit_code = main()

        self.assertEqual(exit_code, 0)
        fake_app.cleanup.assert_called_once()

        time_mock.sleep.assert_called_once_with(args.frequency)

    @mock.patch("raindrip.cli.time")
    @mock.patch("raindrip.cli.parse_args")
    @mock.patch("raindrip.cli.create_app")
    @mock.patch("raindrip.cli.publish_messages")
    def test_main_unknown_error(self, publish_messages, create_app_mock, parse_args_mock, time_mock):
        fake_app = create_app_mock.return_value

        args = mock.MagicMock(command="publisher", loglevel="INFO")
        parse_args_mock.return_value = args

        # to break the loop
        publish_messages.side_effect = Exception()

        with self.assertLogs(level="ERROR") as cm:
            exit_code = main()

        self.assertRegex(cm.output[0], "ERROR:raindrip:\nTraceback")
        self.assertRegex(cm.output[1], "ERROR:raindrip:Abruptly stopping publisher")

        self.assertEqual(exit_code, 1, "Should return non-zero exit code")
        fake_app.cleanup.assert_called_once()
