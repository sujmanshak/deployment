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
import json

from flask import Flask, jsonify, abort, render_template, make_response
from flask_restful import reqparse, Api, Resource, marshal, fields, request
import socket
from Validation import *


APP = Flask(__name__, template_folder="../templates", static_folder="../static")
api = Api(APP)


SERVERS = []
IS_CURRENT_NODE_ADDED = False

server_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'hostname': fields.String,
    'description': fields.String,
    'enabled': fields.Boolean,
    'external-interface': fields.String,
    'internal-interface': fields.String,
    'public-interface': fields.String,
    'client-listener': fields.String,
    'internal-listener': fields.String,
    'admin-listener': fields.String,
    'http-listener': fields.String,
    'replication-listener': fields.String,
    'zookeeper-listener': fields.String,
    'placement-group': fields.String

}


@APP.route("/")
def index():
    """Main Page"""
    return render_template("index.html")


def abort_if_server_doesnt_exist(id):
    """abort"""
    server = [server for server in SERVERS if server['id'] == id]
    if len(server) == 0:
        abort(404, message="Server {} doesn't exist".format(id))


def make_public_server(servers):
    """Server"""
    new_server = {}
    for field in servers:
        new_server[field] = servers[field]
    return new_server


class Server(Resource):
    """shows a single Server item and lets you delete a Server item"""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True,
                                   help='name is required', location='json')
        self.reqparse.add_argument('hostname', type=str, required=True,
                                   help='hostname is required', location='json')
        self.reqparse.add_argument('description', type=str,
                                   default="", location='json')
        self.reqparse.add_argument('enabled', type=bool, default=True, location='json')
        self.reqparse.add_argument('external-interface', type=str, default="", location='json')
        self.reqparse.add_argument('internal-interface', type=str, default="", location='json')
        self.reqparse.add_argument('public-interface', type=str, default="", location='json')
        self.reqparse.add_argument('client-listener', type=str, default="", location='json')
        self.reqparse.add_argument('internal-listener', type=str, default="", location='json')
        self.reqparse.add_argument('admin-listener', type=str, default="", location='json')
        self.reqparse.add_argument('http-listener', type=str, default="", location='json')
        self.reqparse.add_argument('replication-listener', type=str, default="", location='json')
        self.reqparse.add_argument('zookeeper-listener', type=str, default="", location='json')
        self.reqparse.add_argument('placement-group', type=str, default="", location='json')
        super(Server, self).__init__()

    @staticmethod
    def get(id):
        "get server"
        abort_if_server_doesnt_exist(id)
        server = [server for server in SERVERS if server['id'] == id]
        return jsonify({'server': make_public_server(server[0])})

    @staticmethod
    def delete(id):
        """Delete Server"""
        abort_if_server_doesnt_exist(id)
        server = [server for server in SERVERS if server['id'] == id]
        if len(server) == 0:
            abort(404)
        SERVERS.remove(server[0])
        return jsonify({'result': True})

    def put(self, id):
        "Update server"
        server = [server for server in SERVERS if server['id'] == id]
        if len(server) == 0:
            abort(404)
        server = server[0]
        response = Validation.validate_ports_info(request)
        if response['status'] == -1:
            return make_response(jsonify({'error': response['error']}), 404)

        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                server[k] = v
        # return {'server': marshal(server, server_fields)}
        return {'server': server, 'status': 1}


class ServerList(Resource):
    """shows a list of all SERVERS, and lets you POST to add new servers"""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True,
                                   help='name is required', location='json')
        self.reqparse.add_argument('hostname', type=str, required=True,
                                   help='hostname is required', location='json')
        self.reqparse.add_argument('description', type=str,
                                   default="", location='json')
        self.reqparse.add_argument('enabled', type=bool, default=True, location='json')
        self.reqparse.add_argument('external-interface', type=str, default="", location='json')
        self.reqparse.add_argument('internal-interface', type=str, default="", location='json')
        self.reqparse.add_argument('public-interface', type=str, default="", location='json')
        self.reqparse.add_argument('client-listener', type=str, default="", location='json')
        self.reqparse.add_argument('internal-listener', type=str, default="", location='json')
        self.reqparse.add_argument('admin-listener', type=str, default="", location='json')
        self.reqparse.add_argument('http-listener', type=str, default="", location='json')
        self.reqparse.add_argument('replication-listener', type=str, default="", location='json')
        self.reqparse.add_argument('zookeeper-listener', type=str, default="", location='json')
        self.reqparse.add_argument('placement-group', type=str, default="", location='json')
        super(ServerList, self).__init__()

    @staticmethod
    def get():
        """get server"""
        global IS_CURRENT_NODE_ADDED
        my_host_name = socket.gethostname()
        my_host_or_ip = socket.gethostbyname(my_host_name)

        if not SERVERS and not IS_CURRENT_NODE_ADDED:
            IS_CURRENT_NODE_ADDED = True
            SERVERS.append(
                {
                    'id': 1,
                    'name': my_host_name,
                    'hostname': my_host_or_ip,
                    'description': "",
                    'enabled': True,
                    'external-interface': "",
                    'internal-interface': "",
                    'public-interface': "",
                    'client-listener': "",
                    'internal-listener': "",
                    'admin-listener': "",
                    'http-listener': "",
                    'replication-listener': "",
                    'zookeeper-listener': "",
                    'placement-group': ""
                }
            )

        return jsonify({'servers': [make_public_server(x) for x in SERVERS]})

    def post(self):
        """create server"""

        args = self.reqparse.parse_args()

        if args['name'] == "":
            return make_response(jsonify({'error': 'Server name is required'}), 404)

        if args['hostname'] == "":
            return make_response(jsonify({'error': 'Host name is required'}), 404)

        server = [server for server in SERVERS if server['name'] == args['name']]
        if len(server) > 0:
            return make_response(jsonify({'error': 'Server name already exists'}), 404)

        server = [server for server in SERVERS if server['hostname'] == args['hostname']]
        if len(server) > 0:
            return make_response(jsonify({'error': 'Host name already exists'}), 404)

        response = Validation.validate_ports_info(request)
        if response['status'] == -1:
            return make_response(jsonify({'error': response['error']}), 404)

        if not SERVERS:
            server_id = 1
        else:
            server_id = SERVERS[-1]['id'] + 1
        server = {
            'id': server_id,
            'name': args['name'],
            'description': args['description'],
            'hostname': args['hostname'],
            'enabled': True,
            'admin-listener': args['admin-listener'],
            'zookeeper-listener': args['zookeeper-listener'],
            'replication-listener': args['replication-listener'],
            'client-listener': args['client-listener'],
            'internal-interface': args['internal-interface'],
            'external-interface': args['external-interface'],
            'public-interface': args['public-interface'],
            'internal-listener': args['internal-listener'],
            'http-listener': args['http-listener'],
            'placement-group': args['placement-group'],

        }
        SERVERS.append(server)
        return {'server': server, 'status': 1}, 201


api.add_resource(ServerList, '/api/1.0/servers/', endpoint='servers')
api.add_resource(Server, '/api/1.0/servers/<int:id>', endpoint='server')

if __name__ == '__main__':
    APP.run(threaded=True, host='0.0.0.0', port=8000)
