"""
    Some basic tests using Apache "requests" module
    (http://docs.python-requests.org/en/latest/index.html) to handle
    simple communications with the server.

    Get "requests": $ easy_install requests or download the module
    and then install.

    In "setUp", make the request and get the response. Then the
    tests are all specific assertions about the result.

    The requests could be in the tests themselves. There are pluses
    and minuses in all the different possible approaches.

    Next steps -- we can consider this approach, consider "pytest"
    instead of "unittest", and review other options.

    I'll convert this to pytest and we can see if that's better or
    worse or just different.
"""

import requests
import json
import unittest

class TestREST( unittest.TestCase ):
    def setUp(self):
        self.localurl = "http://localhost:8000/api/1.0/servers"
        self.response = requests.get(self.localurl)

    def test_1_get_connect(self):
        self.assertEqual(200, self.response.status_code)

    def test_2_get_servers(self):
        jsonContent = self.response.json()
        self.assertTrue("servers" in jsonContent)

    def test_3_get_server_count(self):
        jsonContent = self.response.json()
        print jsonContent["servers"]
        self.assertTrue(len(jsonContent["servers"]) == 3,
                "Expected 3 servers. Found " + str(len(jsonContent["servers"])))

if __name__ == '__main__':
    unittest.main()
