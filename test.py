import requests
import unittest
import json

TEST_USER_IDN = '5eO--G0jgenNU9Z'

class WebAppTest(unittest.TestCase):
    def test_get_request(self):
        urls = (
                'http://127.0.0.1:8000/',
                'http://127.0.0.1:8000/register/',
                'http://127.0.0.1:8000/login',
                f'http://127.0.0.1:8000/{TEST_USER_IDN}/main',
        )
        status = []

        for u in urls:
            response = requests.get(u)
            status.append(response.status_code)

        exp = [200, 200, 200]
        self.assertEqual(status, [200, 200, 200, 200], f'{status} not equal {exp}')


    def test_post_request(self):
        url = f'http://127.0.0.1:8000/login/'
        resp = requests.post(url, {'username': 'Dendy_981', 'password': 'dendy123'})

        # Status code will always 403 because form also contain csrf_token that changed each time
        # when form was sent

        self.assertEqual(resp.status_code, 403)


if __name__ == '__main__':
    unittest.main()






