import json
import unittest

from functions.api.handler import error_resp


class ApiTest(unittest.TestCase):

    def test_error_resp(self):
        input_ = (200, "test_msg")

        expected = {
            'statusCode': 200,
            'body': json.dumps({
                'error': "test_msg"
            })
        }
        self.assertEqual(expected, error_resp(input_[0], input_[1]))


if __name__ == '__main__':
    unittest.main()
