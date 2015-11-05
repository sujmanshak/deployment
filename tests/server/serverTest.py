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

############VARS

URL = 'http://localhost:8000/api/1.0/servers/'

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

class ServerTest1(TestCase):

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

   #ensure servers are added properly

    def test_04CreateServer(self):
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data={'description':'test','hostname':'test','name':'test'}
        response = requests.post(URL,json=data, headers = headers)
        if response.status_code==201:
            self.assertEqual(response.status_code, 201)
        else:
            self.assertEqual(response.status_code, 404)

    #ensure servers are deleted properly
    def test_08DeleteServer(self):
        #Create a server to delete
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data={'description':'test','hostname':'test','name':'test'}
        response = requests.post(URL,json=data, headers = headers)
        if response.status_code==201:
            self.assertEqual(response.status_code, 201)
        else:
            self.assertEqual(response.status_code, 404)

        #get a serverId
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

class ServerTest2(Server):
    #ensure Duplicate Server name is not added
    def test_09ValidateDuplicateServerName(self):
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
    def test_10ValidateDuplicateHostName(self):
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

     #ensure servers are updated properly

    def test_11UpdateServers(self):
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


if __name__ == '__main__':
        unittest.main()