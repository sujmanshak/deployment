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

from flask import Flask, render_template, jsonify, abort, make_response, request
from flask.views import MethodView
import socket
from Validation import *

APP = Flask(__name__, template_folder="../templates", static_folder="../static")

SERVERS = []


@APP.errorhandler(400)
def not_found(error):
    """Bad Request"""
    print error
    return make_response(jsonify({'error': 'Bad request'}), 400)


@APP.errorhandler(404)
def not_found(error):
    """Not Found"""
    print error
    return make_response(jsonify({'error': 'Not found'}), 404)


@APP.route("/")
def index():
    """Main Page"""
    return render_template("index.html")


def make_public_server(servers):
    """Server"""
    new_server = {}
    for field in servers:
        new_server[field] = servers[field]
    return new_server


IS_CURRENT_NODE_ADDED = False


class ServerAPI(MethodView):
    """Server Requests"""
    @staticmethod
    def get(server_id):
        """Get Server"""
        global IS_CURRENT_NODE_ADDED
        my_host_name = socket.gethostname()
        my_host_or_ip = socket.gethostbyname(my_host_name)

        if server_id is None:

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
                        "client-listener": "",
                        "internal-listener": "",
                        "admin-listener": "",
                        "http-listener": "",
                        "replication-listener": "",
                        "zookeeper-listener": "",
                        "placement-group": ""
                    }
                )

            # return jsonify({'servers': map(make_public_server, SERVERS)})
            return jsonify({'servers': [make_public_server(x) for x in SERVERS]})
        else:
            # server = filter(lambda t: t['id'] == server_id, SERVERS)
            server = [server for server in SERVERS if server.id == server_id]
            if len(server) == 0:
                abort(404)
            return jsonify({'server': make_public_server(server[0])})

    @staticmethod
    def post():
        """Post Server"""
        if not request.json or not 'name' in request.json or not 'hostname' in request.json:
            abort(400)

        if request.json['name'].strip() == "":
            return make_response(jsonify({'error': 'Server name is required'}), 404)

        if request.json['hostname'].strip() == "":
            return make_response(jsonify({'error': 'Host name is required'}), 404)

        server = [server for server in SERVERS if server['name'] == request.json['name']]
        if len(server) != 0:
            return make_response(jsonify({'error': 'Server name already exists'}), 404)

        server = [server for server in SERVERS if server['hostname'] == request.json['hostname']]
        if len(server) != 0:
            return make_response(jsonify({'error': 'Host name already exists'}), 404)


        response = Validation.validate_ports_info(request)
        if response['status'] == -1:
            return make_response(jsonify({'error': response['error']}), 404)

        if not SERVERS:
            serverid = 1
        else:
            serverid = SERVERS[-1]['id'] + 1
        server = {
            'id': serverid,
            'name': request.json['name'].strip(),
            'description': request.json.get('description', "").strip(),
            'hostname': request.json.get('hostname', "").strip(),
            'enabled': True,
            'admin-listener': request.json.get('admin-listener', "").strip(),
            'zookeeper-listener': request.json.get('zookeeper-listener', "").strip(),
            'replication-listener': request.json.get('replication-listener', "").strip(),
            'client-listener': request.json.get('client-listener', "").strip(),
            'internal-interface': request.json.get('internal-interface', "").strip(),
            'external-interface': request.json.get('external-interface', "").strip(),
            'public-interface': request.json.get('public-interface', "").strip(),
            'internal-listener': request.json.get('internal-listener', "").strip(),
            'http-listener': request.json.get('http-listener', "").strip(),
            "placement-group": request.json.get('placement-group', "").strip(),

        }
        SERVERS.append(server)
        return jsonify({'server': server, 'status': 1}), 201

    @staticmethod
    def delete(server_id):
        """Delete Server"""
        server = [server for server in SERVERS if server['id'] == server_id]
        if len(server) == 0:
            abort(404)
        SERVERS.remove(server[0])
        return jsonify({'result': True})

    @staticmethod
    def put(server_id):
        """Put Server"""

        current_server = [server for server in SERVERS if server['id'] == server_id]
        if len(current_server) == 0:
            abort(404)
        if not request.json:
            abort(400)
        if 'name' in request.json and not isinstance(request.json['name'], unicode):
            abort(400)
        if 'description' in request.json and not isinstance(request.json['description'], unicode):
            abort(400)
        if 'enabled' in request.json and not isinstance(request.json['enabled'], bool):
            abort(400)
        if 'hostname' in request.json and not isinstance(request.json['hostname'], unicode):
            abort(400)

        if 'name' in request.json:
            if request.json['name'].strip() == "":
                return make_response(jsonify({'error': 'Server name is required'}), 404)

        if 'hostname' in request.json:
            if request.json['hostname'].strip() == "":
                return make_response(jsonify({'error': 'Host name is required'}), 404)

        response = Validation.validate_ports_info(request)
        if response['status'] == -1:
            return make_response(jsonify({'error': response['error']}), 404)

        current_server[0]['name'] = request.json.get('name',
                                                     current_server[0]['name']).strip()
        current_server[0]['hostname'] = request.json.get('hostname',
                                                         current_server[0]['hostname']).strip()
        current_server[0]['description'] = request.json.get \
            ('description', current_server[0]['description']).strip()
        current_server[0]['enabled'] = request.json.get \
            ('enabled', current_server[0]['enabled'])
        current_server[0]['admin-listener'] = request.json.get \
            ('admin-listener', current_server[0]['admin-listener']).strip()
        current_server[0]['internal-listener'] = request.json.get \
            ('internal-listener', current_server[0]['internal-listener']).strip()
        current_server[0]['http-listener'] = request.json.get \
            ('http-listener', current_server[0]['http-listener']).strip()
        current_server[0]['zookeeper-listener'] = request.json.get \
            ('zookeeper-listener', current_server[0]['zookeeper-listener']).strip()
        current_server[0]['replication-listener'] = request.json.get \
            ('replication-listener', current_server[0]['replication-listener']).strip()
        current_server[0]['client-listener'] = request.json.get \
            ('client-listener', current_server[0]['client-listener']).strip()
        current_server[0]['internal-interface'] = request.json.get \
            ('internal-interface', current_server[0]['internal-interface']).strip()
        current_server[0]['external-interface'] = request.json.get \
            ('external-interface', current_server[0]['external-interface']).strip()
        current_server[0]['public-interface'] = request.json.get\
            ('public-interface', current_server[0]['public-interface']).strip()
        current_server[0]['placement-group'] = request.json.get\
            ('placement-group', current_server[0]['placement-group']).strip()
        return jsonify({'server': current_server[0], 'status': 1})


if __name__ == '__main__':
    APP.config.update(
        DEBUG=True,
    )
    SERVER_VIEW = ServerAPI.as_view('server_api')
    APP.add_url_rule('/api/1.0/servers/', defaults={'server_id': None},
                     view_func=SERVER_VIEW, methods=['GET', ])
    APP.add_url_rule('/api/1.0/servers/', view_func=SERVER_VIEW, methods=['POST', ])
    APP.add_url_rule('/api/1.0/servers/<int:server_id>', view_func=SERVER_VIEW,
                     methods=['GET', 'PUT', 'DELETE'])

    APP.run(threaded=True, host='0.0.0.0', port=8000)
