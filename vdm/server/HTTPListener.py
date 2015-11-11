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


from flask import Flask, render_template, jsonify, abort, make_response, request
from flask.views import MethodView

import socket
import fcntl
import struct
import re

app = Flask(__name__, template_folder ="../templates", static_folder="../static")


servers = []



@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route("/")
def index():
    return render_template("index.html")

def make_public_server(servers):
    new_server = {}
    for field in servers:
        new_server[field] = servers[field]
    return new_server

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

isCurrentNodeAdded = False

class ServerAPI(MethodView):

    def get(self, server_id):
        global isCurrentNodeAdded
        hostname =  get_ip_address('eth0')

        if server_id is None:

            if not servers and isCurrentNodeAdded==False:
                #add default server
                isCurrentNodeAdded = True
                servers.append(
                    {
                        'id': 1,
                        'name': hostname,
                        'hostname': hostname,
                        'description': "",
                        'enabled': True,
                        'externalinterface': "",
                        'internalinterface': "",
                        'publicinterface':"",
                        "clientlistener":"",
                        "adminlistener":"",
                        "replicationlistener":"",
                        "zookeeperlistener":"",
                        # 'http': "8080",
                        # 'internalport': "3021",
                        # 'portname': "21223",
                        # 'replicationport': "5555",
                        # 'zookeeper': "2181"
                    }
                    )

            # return a list of users
            return jsonify( { 'servers': map(make_public_server, servers) } )
        else:
            # expose a single user
            server = filter(lambda t: t['id'] == server_id, servers)
            if len(server) == 0:
                abort(404)
            return jsonify( { 'server': make_public_server(server[0]) } )

    def post(self):
        if not request.json or not 'name' in request.json or not 'hostname' in request.json:
            abort(400)

        if request.json['name']=="":
            return make_response(jsonify({'error':'Server name is required'}),404)

        if request.json['hostname']=="":
            return make_response(jsonify({'error':'Host name is required'}),404)

        server = filter(lambda t: t['name'] == request.json['name'], servers)
        if len(server)!=0:
            return make_response(jsonify({'error': 'Server name already exists'}), 404)

        server = filter(lambda t: t['hostname'] == request.json['hostname'], servers)
        if len(server)!=0:
            return make_response(jsonify({'error': 'Host name already exists'}), 404)

        if 'adminlistener' in request.json:
            if(request.json['adminlistener']!=""):
                if(":" in request.json['adminlistener']):
                    count =  request.json['adminlistener'].count(":")
                    print "test" + str(count)
                    if(count>1):
                       return make_response(jsonify({'error': 'Invalid admin listener'}), 404)
                    #validate both ip as well as port
                    array =  request.json['adminlistener'].split(":")
                    try:
                        socket.inet_aton(array[0])
                    # legal
                    except socket.error:
                        return make_response(jsonify({'error': 'Invalid IP address'}), 404)

                    #validate port only
                    try:
                        val = int(array[1])
                        if val<0:
                            return make_response(jsonify({'error': 'Admin Listener must be a positive number'}), 404)
                        elif val<1 or val>=65535:
                            return make_response(jsonify({'error': 'Admin Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Admin Listener must be a positive number'}), 404)

                else:
                    try:
                        val = int(request.json['adminlistener'])
                        if val<0:
                            return make_response(jsonify({'error': 'Admin Listener must be a positive number'}), 404)
                        elif val<1 or val>65536:
                            return make_response(jsonify({'error': 'Admin Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Admin Listener must be a positive number'}), 404)

        if 'zookeeperlistener' in request.json:
            if(request.json['zookeeperlistener']!=""):
                if(":" in request.json['zookeeperlistener']):
                    count =  request.json['zookeeperlistener'].count(":")
                    print "test" + str(count)
                    if(count>1):
                       return make_response(jsonify({'error': 'Invalid Zookeeper listener'}), 404)
                    #validate both ip as well as port
                    array =  request.json['zookeeperlistener'].split(":")
                    try:
                        socket.inet_aton(array[0])
                    # legal
                    except socket.error:
                        return make_response(jsonify({'error': 'Invalid IP address'}), 404)

                    #validate port only
                    try:
                        val = int(array[1])
                        if val<0:
                            return make_response(jsonify({'error': 'Zookeeper Listener must be a positive number'}), 404)
                        elif val<1 or val>=65535:
                            return make_response(jsonify({'error': 'Zookeeper Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Zookeeper Listener must be a positive number'}), 404)

                else:
                    try:
                        val = int(request.json['zookeeperlistener'])
                        if val<0:
                            return make_response(jsonify({'error': 'Zookeeper Listener must be a positive number'}), 404)
                        elif val<1 or val>65536:
                            return make_response(jsonify({'error': 'Zookeeper Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Zookeeper Listener must be a positive number'}), 404)

        if 'replicationlistener' in request.json:
            if(request.json['replicationlistener']!=""):
                if(":" in request.json['replicationlistener']):
                    count =  request.json['replicationlistener'].count(":")
                    print "test" + str(count)
                    if(count>1):
                       return make_response(jsonify({'error': 'Invalid Replicationlistener'}), 404)
                    #validate both ip as well as port
                    array =  request.json['replicationlistener'].split(":")
                    try:
                        socket.inet_aton(array[0])
                    # legal
                    except socket.error:
                        return make_response(jsonify({'error': 'Invalid IP address'}), 404)

                    #validate port only
                    try:
                        val = int(array[1])
                        if val<0:
                            return make_response(jsonify({'error': 'Replication Listener must be a positive number'}), 404)
                        elif val<1 or val>=65535:
                            return make_response(jsonify({'error': 'Replication Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Replication Listener must be a positive number'}), 404)

                else:
                    try:
                        val = int(request.json['replicationlistener'])
                        if val<0:
                            return make_response(jsonify({'error': 'Replication Listener must be a positive number'}), 404)
                        elif val<1 or val>65536:
                            return make_response(jsonify({'error': 'Replication Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Replication Listener must be a positive number'}), 404)

        if 'clientlistener' in request.json:
            if(request.json['clientlistener']!=""):
                if(":" in request.json['clientlistener']):
                    count =  request.json['clientlistener'].count(":")
                    print "test" + str(count)
                    if(count>1):
                       return make_response(jsonify({'error': 'Invalid Client listener'}), 404)
                    #validate both ip as well as port
                    array =  request.json['clientlistener'].split(":")
                    try:
                        socket.inet_aton(array[0])
                    # legal
                    except socket.error:
                        return make_response(jsonify({'error': 'Invalid IP address'}), 404)

                    #validate port only
                    try:
                        val = int(array[1])
                        if val<0:
                            return make_response(jsonify({'error': 'Client Listener must be a positive number'}), 404)
                        elif val<1 or val>=65535:
                            return make_response(jsonify({'error': 'Client Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Client Listener must be a positive number'}), 404)

                else:
                    try:
                        val = int(request.json['clientlistener'])
                        if val<0:
                            return make_response(jsonify({'error': 'Client Listener must be a positive number'}), 404)
                        elif val<1 or val>65536:
                            return make_response(jsonify({'error': 'Client Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Client Listener must be a positive number'}), 404)

        if 'internalinterface' in request.json:
            if (request.json['internalinterface']!=""):
                try:
                    socket.inet_aton(request.json['internalinterface'])
                except socket.error:
                    return make_response(jsonify({'error': 'Invalid IP address'}), 404)

        if 'externalinterface' in request.json:
            if (request.json['externalinterface']!=""):
                try:
                    socket.inet_aton(request.json['externalinterface'])
                except socket.error:
                    return make_response(jsonify({'error': 'Invalid IP address'}), 404)

        if 'publicinterface' in request.json:
            if (request.json['publicinterface']!=""):
                try:
                    socket.inet_aton(request.json['publicinterface'])
                except socket.error:
                    return make_response(jsonify({'error': 'Invalid IP address'}), 404)


        serverId = 0
        if not servers:
            serverId = 1
        else:
            serverId = servers[-1]['id'] + 1
        server = {
        'id': serverId,
        'name': request.json['name'],
        'description': request.json.get('description', ""),
        'hostname': request.json.get('hostname', ""),
        'enabled': True,
        'adminlistener': request.json.get('adminlistener',""),
        'zookeeperlistener': request.json.get('zookeeperlistener',""),
        'replicationlistener': request.json.get('replicationlistener',""),
        'clientlistener': request.json.get('clientlistener',""),
        'internalinterface': request.json.get('internalinterface',""),
        'externalinterface': request.json.get('externalinterface',""),
        'publicinterface': request.json.get('publicinterface',"")
        }
        servers.append(server)
        return jsonify( { 'server': server, 'status':1 } ),201

    def delete(self, server_id):
        # delete a single server
        server = filter(lambda t: t['id'] == server_id, servers)
        if len(server) == 0:
            abort(404)
        servers.remove(server[0])
        return jsonify( { 'result': True } )

    def put(self, server_id):
        # update a single server
        currentserver = filter(lambda t: t['id'] == server_id, servers)
        if len(currentserver) == 0:
            abort(404)
        if not request.json:
            abort(400)
        if 'name' in request.json and type(request.json['name']) != unicode:
            abort(400)
        if 'description' in request.json and type(request.json['description']) is not unicode:
            abort(400)
        if 'enabled' in request.json and type(request.json['enabled']) is not bool:
            abort(400)
        if 'hostname' in request.json and type(request.json['hostname']) is not unicode:
            abort(400)

        if 'name' in request.json:
            if request.json['name']=="":
                return make_response(jsonify({'error':'Server name is required'}),404)

            if request.json['name']!= currentserver[0]['name']:
                server = filter(lambda t: t['name'] == request.json['name'], servers)
                # if len(server)!=0:
                #     return make_response(jsonify({'error': 'Server name already exists'}), 404)

        if 'hostname' in request.json:
            if request.json['hostname']==   "":
                return make_response(jsonify({'error':'Host name is required'}),404)
            server = filter(lambda t: t['hostname'] == request.json['hostname'], servers)
            # if len(server)!=0:
            #     return make_response(jsonify({'error': 'Host name already exists'}), 404)

        if 'adminlistener' in request.json:
            if(request.json['adminlistener']!=""):
                if(":" in request.json['adminlistener']):
                    count =  request.json['adminlistener'].count(":")
                    print "test" + str(count)
                    if(count>1):
                       return make_response(jsonify({'error': 'Invalid admin listener'}), 404)
                    #validate both ip as well as port
                    array =  request.json['adminlistener'].split(":")
                    try:
                        socket.inet_aton(array[0])
                    # legal
                    except socket.error:
                        return make_response(jsonify({'error': 'Invalid IP address'}), 404)

                    #validate port only
                    try:
                        val = int(array[1])
                        if val<0:
                            return make_response(jsonify({'error': 'Admin Listener must be a positive number'}), 404)
                        elif val<1 or val>=65535:
                            return make_response(jsonify({'error': 'Admin Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Admin Listener must be a positive number'}), 404)

                else:
                    try:
                        val = int(request.json['adminlistener'])
                        if val<0:
                            return make_response(jsonify({'error': 'Admin Listener must be a positive number'}), 404)
                        elif val<1 or val>65536:
                            return make_response(jsonify({'error': 'Admin Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Admin Listener must be a positive number'}), 404)

        if 'zookeeperlistener' in request.json:
            if(request.json['zookeeperlistener']!=""):
                if(":" in request.json['zookeeperlistener']):
                    count =  request.json['zookeeperlistener'].count(":")
                    print "test" + str(count)
                    if(count>1):
                       return make_response(jsonify({'error': 'Invalid Zookeeper listener'}), 404)
                    #validate both ip as well as port
                    array =  request.json['zookeeperlistener'].split(":")
                    try:
                        socket.inet_aton(array[0])
                    # legal
                    except socket.error:
                        return make_response(jsonify({'error': 'Invalid IP address'}), 404)

                    #validate port only
                    try:
                        val = int(array[1])
                        if val<0:
                            return make_response(jsonify({'error': 'Zookeeper Listener must be a positive number'}), 404)
                        elif val<1 or val>=65535:
                            return make_response(jsonify({'error': 'Zookeeper Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Zookeeper Listener must be a positive number'}), 404)

                else:
                    try:
                        val = int(request.json['zookeeperlistener'])
                        if val<0:
                            return make_response(jsonify({'error': 'Zookeeper Listener must be a positive number'}), 404)
                        elif val<1 or val>65536:
                            return make_response(jsonify({'error': 'Zookeeper Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Zookeeper Listener must be a positive number'}), 404)

        if 'replicationlistener' in request.json:
            if(request.json['replicationlistener']!=""):
                if(":" in request.json['replicationlistener']):
                    count =  request.json['replicationlistener'].count(":")
                    print "test" + str(count)
                    if(count>1):
                       return make_response(jsonify({'error': 'Invalid Replicationlistener'}), 404)
                    #validate both ip as well as port
                    array =  request.json['replicationlistener'].split(":")
                    try:
                        socket.inet_aton(array[0])
                    # legal
                    except socket.error:
                        return make_response(jsonify({'error': 'Invalid IP address'}), 404)

                    #validate port only
                    try:
                        val = int(array[1])
                        if val<0:
                            return make_response(jsonify({'error': 'Replication Listener must be a positive number'}), 404)
                        elif val<1 or val>=65535:
                            return make_response(jsonify({'error': 'Replication Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Replication Listener must be a positive number'}), 404)

                else:
                    try:
                        val = int(request.json['replicationlistener'])
                        if val<0:
                            return make_response(jsonify({'error': 'Replication Listener must be a positive number'}), 404)
                        elif val<1 or val>65536:
                            return make_response(jsonify({'error': 'Replication Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Replication Listener must be a positive number'}), 404)

        if 'clientlistener' in request.json:
            if(request.json['clientlistener']!=""):
                if(":" in request.json['clientlistener']):
                    count =  request.json['clientlistener'].count(":")
                    print "test" + str(count)
                    if(count>1):
                       return make_response(jsonify({'error': 'Invalid Client listener'}), 404)
                    #validate both ip as well as port
                    array =  request.json['clientlistener'].split(":")
                    try:
                        socket.inet_aton(array[0])
                    # legal
                    except socket.error:
                        return make_response(jsonify({'error': 'Invalid IP address'}), 404)

                    #validate port only
                    try:
                        val = int(array[1])
                        if val<0:
                            return make_response(jsonify({'error': 'Client Listener must be a positive number'}), 404)
                        elif val<1 or val>=65535:
                            return make_response(jsonify({'error': 'Client Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Client Listener must be a positive number'}), 404)

                else:
                    try:
                        val = int(request.json['clientlistener'])
                        if val<0:
                            return make_response(jsonify({'error': 'Client Listener must be a positive number'}), 404)
                        elif val<1 or val>65536:
                            return make_response(jsonify({'error': 'Client Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Client Listener must be a positive number'}), 404)

        if 'internalinterface' in request.json:
            if (request.json['internalinterface']!=""):
                try:
                    socket.inet_aton(request.json['internalinterface'])
                    # legal
                except socket.error:
                    return make_response(jsonify({'error': 'Invalid IP address'}), 404)

        if 'externalinterface' in request.json:
            if (request.json['externalinterface']!=""):
                try:
                    socket.inet_aton(request.json['externalinterface'])
                    # legal
                except socket.error:
                    return make_response(jsonify({'error': 'Invalid IP address'}), 404)

        if 'publicinterface' in request.json:
            if (request.json['publicinterface']!=""):
                try:
                    socket.inet_aton(request.json['publicinterface'])
                except socket.error:
                    return make_response(jsonify({'error': 'Invalid IP address'}), 404)

        currentserver[0]['name'] = request.json.get('name', currentserver[0]['name'])
        currentserver[0]['hostname'] = request.json.get('hostname', currentserver[0]['hostname'])
        currentserver[0]['description'] = request.json.get('description', currentserver[0]['description'])
        currentserver[0]['enabled'] = request.json.get('enabled', currentserver[0]['enabled'])
        currentserver[0]['adminlistener'] = request.json.get('adminlistener', currentserver[0]['adminlistener'])
        currentserver[0]['zookeeperlistener'] = request.json.get('zookeeperlistener', currentserver[0]['zookeeperlistener'])
        currentserver[0]['replicationlistener'] = request.json.get('replicationlistener', currentserver[0]['replicationlistener'])
        currentserver[0]['clientlistener'] = request.json.get('clientlistener', currentserver[0]['clientlistener'])
        currentserver[0]['internalinterface'] = request.json.get('internalinterface', currentserver[0]['internalinterface'])
        currentserver[0]['externalinterface'] = request.json.get('externalinterface', currentserver[0]['externalinterface'])
        currentserver[0]['publicinterface'] = request.json.get('publicinterface', currentserver[0]['publicinterface'])
        return jsonify( { 'server': currentserver[0], 'status': 1} )


if __name__ == '__main__':
    app.config.update(
        DEBUG=True,
    );
    server_view = ServerAPI.as_view('server_api')
    app.add_url_rule('/api/1.0/servers/', defaults={'server_id': None},
                     view_func=server_view, methods=['GET',])
    app.add_url_rule('/api/1.0/servers/', view_func=server_view, methods=['POST',])
    app.add_url_rule('/api/1.0/servers/<int:server_id>', view_func=server_view,
                     methods=['GET', 'PUT', 'DELETE'])

    app.run(threaded=True, host='0.0.0.0', port=8000)
