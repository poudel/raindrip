from unittest import TestCase, mock
from raindrip.config import env


class TestConfig(TestCase):

    @mock.patch("os.environ")
    def test_env(self, environ_mock):
        value = env("ASDF")

        environ_mock.get.assert_called_once_with("ASDF")
        self.assertEqual(value, environ_mock.get.return_value)

    def test_env_default(self):
        value = env("key", "default")
        self.assertEqual(value, "default")

    @mock.patch("os.environ")
    def test_env_raises_RuntimeError(self, environ_mock):
        environ_mock.get.return_value = None

        with self.assertRaises(RuntimeError):
            env("ASDF")
