import unittest
from capless.publish.client import Publish


class PublishTestCase(unittest.TestCase):
    def setUp(self):
        self.config_path = 'publish.yml'

    def test_publish_init(self):
        publish = Publish(config_path=self.config_path)


if __name__ == '__main__':
    unittest.main()
