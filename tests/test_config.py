from unittest import TestCase, mock
from raindrip.config import Config


class TestConfig(TestCase):

    @mock.patch("raindrip.config.os")
    def test_from_environment(self, os_mock):
        os_mock.environ = {
        }

        Config.from_environment()
