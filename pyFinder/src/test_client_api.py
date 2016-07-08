import unittest
from .pyDescriptor import ClientApi


class ClientApiTestCase(unittest.TestCase):
    "tests  for `client_api.py`"

    def test_get_images(self):
        ClientApi.post_image({"repo_name":"prova", "bins": [
            {
                "bin": "python",
                "ver": "2.7.6"
            },
            {
                "bin": "python3",
                "ver": "3.4.3"
            }]})
        #ClientApi.ge