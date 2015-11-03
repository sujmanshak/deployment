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

class ServerTest(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    #ensure GET server list
    def test_GetServers(self):
        response = requests.get(URL)
        value= response.json()
        if not value:
            print "The Server list is empty"
        self.assertEqual(response.status_code, 200)

    #ensure servers are added properly
    def test_CreateServer(self):
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data={'description':'test','hostname':'test','name':'test'}
        response = requests.post(URL,json=data, headers = headers)
        self.assertEqual(response.status_code, 201)


    #ensure servers are updated properly
    def test_UpdateServers(self):
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


    #ensure servers are deleted propery
    def test_DeleteServer(self):
        #get a serverId
        response= requests.get(URL)
        value= response.json()
        if value:
            serverLength = len(value['servers'])
            lastServerId =  value['servers'][serverLength-1]['id']
            print "ServerId to be deleted is " + str(lastServerId)
            url = 'http://localhost:8000/api/1.0/servers/' + str(lastServerId)
            response = requests.delete(url)
            self.assertEqual(response.status_code,200)
        else:
            print "The Server list is empty"



if __name__ == '__main__':
        unittest.main()