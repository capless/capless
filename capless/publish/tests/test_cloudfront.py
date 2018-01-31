import unittest
from capless.publish.cf import CloudFront


class CloudFrontTestCase(unittest.TestCase):
    def setUp(self):
        self.config_path = 'app.yml'

    def test_publish_init(self):
        publish = CloudFront(config_path=self.config_path)
        print(publish.to_json())


if __name__ == '__main__':
    unittest.main()
