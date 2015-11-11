# This file is part of VoltDB.

# Copyright (C) 2008-2015 VoltDB Inc.
#
# This file contains original code and/or modifications of original code.
# Any modifications made by VoltDB Inc. are licensed under the following
# terms and conditions:
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

"""
    This test requires installation of flask-Testing from http://pythonhosted.org/Flask-Testing/
    To install flask-Testing use command:
    pip install Flask-Testing


    This test also requires installation of requests library https://pypi.python.org/pypi/requests/
    To install latest requests version 2.8.1 use command:

    sudo pip install requests --upgrade
"""

from flask import Flask
import unittest
from flask.ext.testing import TestCase
import requests
import xmlrunner
import socket
import fcntl
import struct

############VARS

URL = 'http://localhost:8000/api/1.0/servers/'

def get_ip_address(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
        )[20:24])

class Server(unittest.TestCase):
    def setUp(self):
        #Create a server
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data={'description':'test','hostname':'test','name':'test'}
        response = requests.post(URL,json=data, headers = headers)
        if response.status_code==201:
            self.assertEqual(response.status_code, 201)
        else:
            self.assertEqual(response.status_code, 404)
    def tearDown(self):
        #Delete the server
        response= requests.get(URL)
        value= response.json()
        if value:
            serverLength = len(value['servers'])
            lastServerId =  value['servers'][serverLength-1]['id']
            print "ServerId to be deleted is " + str(lastServerId)
            url = URL + str(lastServerId)
            response = requests.delete(url)
            self.assertEqual(response.status_code,200)
        else:
            print "The Server list is empty"


class CreateServer(Server):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

     #ensure GET server list
    def test_01GetServers(self):
        response = requests.get(URL)
        value= response.json()
        if not value:
            print "The Server list is empty"
        self.assertEqual(response.status_code, 200)

    #ensure server name is not empty
    def test_02ValidateServername(self):
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data={'description':'test','hostname':'test','name':''}
        response = requests.post(URL,json=data, headers = headers)
        value=response.json()
        self.assertEqual(value['error'],'Server name is required')
        self.assertEqual(response.status_code, 404)

    #ensure server name is not empty
    def test_03ValidateHostname(self):
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data={'description':'test','hostname':'','name':'test'}
        response = requests.post(URL,json=data, headers = headers)
        value=response.json()
        self.assertEqual(value['error'],'Host name is required')
        self.assertEqual(response.status_code, 404)

    #ensure Duplicate Server name is not added
    def test_04ValidateDuplicateServerName(self):
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data={'description':'test','hostname':'test12345','name':'test'}
        response = requests.post(URL,json=data, headers = headers)
        value=response.json()
        if response.status_code==201:
            print "new server created"
            self.assertEqual(response.status_code, 201)
        else:
            self.assertEqual(response.status_code, 404)
            self.assertEqual(value['error'],'Server name already exists')
            print value['error']

    #ensure Duplicate Host name is not added
    def test_05ValidateDuplicateHostName(self):
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data={'description':'test','hostname':'test','name':'test12345'}
        response = requests.post(URL,json=data, headers = headers)
        value=response.json()
        if response.status_code==201:
            self.assertEqual(response.status_code, 201)
        else:
            self.assertEqual(response.status_code, 404)
            self.assertEqual(value['error'],'Host name already exists')
            print value['error']

class UpdateServer(Server):
    #ensure GET server list
    def test_06GetServers(self):
        response = requests.get(URL)
        value= response.json()
        if not value:
            print "The Server list is empty"
        self.assertEqual(response.status_code, 200)

    #ensure server name is not empty
    def test_07ValidateServername(self):
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data={'description':'test','hostname':'test','name':''}
        response = requests.post(URL,json=data, headers = headers)
        value=response.json()
        self.assertEqual(value['error'],'Server name is required')
        self.assertEqual(response.status_code, 404)

    #ensure server name is not empty
    def test_08ValidateHostname(self):
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data={'description':'test','hostname':'','name':'test'}
        response = requests.post(URL,json=data, headers = headers)
        value=response.json()
        self.assertEqual(value['error'],'Host name is required')
        self.assertEqual(response.status_code, 404)




    def test_09UpdateServers(self):
        #get a serverId
        response= requests.get(URL)
        value= response.json()

        if value:
            serverLength = len(value['servers'])
            lastServerId =  value['servers'][serverLength-1]['id']
            print "ServerId to be updated is " + str(lastServerId)
            url = URL + str(lastServerId)
            response = requests.put(url,json={'description':'ttest123'})
            self.assertEqual(response.status_code,200)
        else:
            print "The Server list is empty"

    #ensure Duplicate Server name is not added
    def test_10ValidateDuplicateServerName(self):
        #get a serverId
        response= requests.get(URL)
        value= response.json()

        if value:
            serverLength = len(value['servers'])
            lastServerId =  value['servers'][serverLength-1]['id']
            print "ServerId to be updated is " + str(lastServerId)
            url = URL + str(lastServerId)

        response = requests.put(url,json={"description":"test","hostname":"test12345","name":get_ip_address('eth0')})
        value = response.json()
        if response.status_code==200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 404)
            self.assertEqual(value['error'],'Server name already exists')

    #ensure Duplicate Host name is not added
    def test_11ValidateDuplicateHostName(self):
        #get a serverId
        response= requests.get(URL)
        value= response.json()

        if value:
            serverLength = len(value['servers'])
            lastServerId =  value['servers'][serverLength-1]['id']
            print "ServerId to be updated is " + str(lastServerId)
            url = URL + str(lastServerId)

        response = requests.put(url,json={'description':'test','hostname':get_ip_address('eth0'),'name':'test12345'})
        value=response.json()
        if response.status_code==200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 404)
            self.assertEqual(value['error'],'Host name already exists')


if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
    unittest.main()
