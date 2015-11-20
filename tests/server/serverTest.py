"""
This file is part of VoltDB.

Copyright (C) 2008-2015 VoltDB Inc.

This file contains original code and/or modifications of original code.
Any modifications made by VoltDB Inc. are licensed under the following
terms and conditions:

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""


import socket
import unittest
import xmlrunner

import requests
from flask import Flask
from flask.ext.testing import TestCase


URL = 'http://localhost:8000/api/1.0/servers/'


class Server(TestCase):
    """common methods"""

    def create_app(self):
        """Create app"""
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def setUp(self):
        """Create a server"""
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data = {'description': 'test', 'hostname': 'test', 'name': 'test'}
        response = requests.post(URL, json=data, headers=headers)
        if response.status_code == 201:
            self.assertEqual(response.status_code, 201)
        else:
            self.assertEqual(response.status_code, 404)

    def tearDown(self):
        """Delete the server"""
        response = requests.get(URL)
        value = response.json()
        if value:
            server_length = len(value['servers'])
            last_server_id = value['servers'][server_length - 1]['id']
            print "ServerId to be deleted is " + str(last_server_id)
            url = URL + str(last_server_id)
            response = requests.delete(url)
            self.assertEqual(response.status_code, 200)
        else:
            print "The Server list is empty"


class CreateServer(Server):
    """Create Server Test cases"""

    def test_get_servers(self):
        """ensure GET server list"""
        response = requests.get(URL)
        value = response.json()
        if not value:
            print "The Server list is empty"
        self.assertEqual(response.status_code, 200)

    def test_validate_server_name(self):
        """ensure server name is not empty"""
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data = {'description': 'test', 'hostname': 'test', 'name': ''}
        response = requests.post(URL, json=data, headers=headers)
        value = response.json()
        self.assertEqual(value['error'], 'Server name is required')
        self.assertEqual(response.status_code, 404)

    def test_validate_hostname(self):
        """ensure server name is not empty"""
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data = {'description': 'test', 'hostname': '', 'name': 'test'}
        response = requests.post(URL, json=data, headers=headers)
        value = response.json()
        self.assertEqual(value['error'], 'Host name is required')
        self.assertEqual(response.status_code, 404)

    def test_validate_duplicate_servername(self):
        """ensure Duplicate Server name is not added"""
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data = {'description': 'test', 'hostname': 'test12345', 'name': 'test'}
        response = requests.post(URL, json=data, headers=headers)
        value = response.json()
        if response.status_code == 201:
            print "new server created"
            self.assertEqual(response.status_code, 201)
        else:
            self.assertEqual(response.status_code, 404)
            self.assertEqual(value['error'], 'Server name already exists')
            print value['error']

    def test_validate_duplicate_host_name(self):
        """ensure Duplicate Host name is not added"""
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data = {'description': 'test', 'hostname': 'test', 'name': 'test12345'}
        response = requests.post(URL, json=data, headers=headers)
        value = response.json()
        if response.status_code == 201:
            self.assertEqual(response.status_code, 201)
        else:
            self.assertEqual(response.status_code, 404)
            self.assertEqual(value['error'], 'Host name already exists')
            print value['error']

    def test_validate_port(self):
        """Validate port"""
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data = {'description': 'test', 'hostname': 'test4567',
                'name': 'test12345', 'adminlistener': '88888'}
        response = requests.post(URL, json=data, headers=headers)
        value = response.json()
        if response.status_code == 201:
            self.assertEqual(response.status_code, 201)
        else:
            self.assertEqual(response.status_code, 404)
            self.assertEqual(value['error'], 'Admin Listener must be '
                                             'greater than 1 and less than 65535')

    def test_validate_ip_address(self):
        """Validate IP Address"""
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data = {'description': 'test', 'hostname': 'test4567', 'name': 'test12345',
                'internalinterface': '127.0.0.12345'}
        response = requests.post(URL, json=data, headers=headers)
        value = response.json()
        if response.status_code == 201:
            self.assertEqual(response.status_code, 201)
        else:
            self.assertEqual(response.status_code, 404)
            self.assertEqual(value['error'], 'Invalid IP address')


class UpdateServer(Server):
    """Update Server test cases"""

    def test_get_servers(self):
        """ensure GET server list"""
        response = requests.get(URL)
        value = response.json()
        if not value:
            print "The Server list is empty"
        self.assertEqual(response.status_code, 200)

    def test_validate_servername(self):
        """ensure server name is not empty"""
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data = {'description': 'test', 'hostname': 'test', 'name': ''}
        response = requests.post(URL, json=data, headers=headers)
        value = response.json()
        self.assertEqual(value['error'], 'Server name is required')
        self.assertEqual(response.status_code, 404)

    def test_validate_hostname(self):
        """ensure server name is not empty"""
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data = {'description': 'test', 'hostname': '', 'name': 'test'}
        response = requests.post(URL, json=data, headers=headers)
        value = response.json()
        self.assertEqual(value['error'], 'Host name is required')
        self.assertEqual(response.status_code, 404)

    def test_update_servers(self):
        """ensure server is updating properly"""

        response = requests.get(URL)
        value = response.json()

        if value:
            server_length = len(value['servers'])
            last_server_id = value['servers'][server_length - 1]['id']
            print "ServerId to be updated is " + str(last_server_id)
            url = URL + str(last_server_id)
            response = requests.put(url, json={'description': 'ttest123'})
            self.assertEqual(response.status_code, 200)
        else:
            print "The Server list is empty"

    def test_validate_duplicate_servername(self):
        """ensure Duplicate Server name is not added"""
        response = requests.get(URL)
        value = response.json()

        if value:
            server_length = len(value['servers'])
            last_server_id = value['servers'][server_length - 1]['id']
            print "ServerId to be updated is " + str(last_server_id)
            url = URL + str(last_server_id)
            my_host_name = socket.gethostname()

        response = requests.put(url, json={"description": "test",
                                           "hostname": "test12345", "name": my_host_name})
        value = response.json()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 404)
            self.assertEqual(value['error'], 'Server name already exists')

    def test_validate_duplicate_host_name(self):
        """ensure Duplicate Host name is not added"""
        response = requests.get(URL)
        value = response.json()

        if value:
            server_length = len(value['servers'])
            last_server_id = value['servers'][server_length - 1]['id']
            print "ServerId to be updated is " + str(last_server_id)
            url = URL + str(last_server_id)
            my_host_name = socket.gethostname()
            my_host_or_ip = socket.gethostbyname(my_host_name)
        response = requests.put(url, json={'description': 'test',
                                           'hostname': my_host_or_ip, 'name': 'test12345'})
        value = response.json()
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 404)
            self.assertEqual(value['error'], 'Host name already exists')


if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
    unittest.main()
