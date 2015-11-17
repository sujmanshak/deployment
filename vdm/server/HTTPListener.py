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

app = Flask(__name__, template_folder ="../templates", static_folder="../static")


servers = []

clusters = [{
    'id': 1,
    "name": "cluster1",
    "deployment" : "default",
    "members": {
        'id' :1,
      "member": { "name": "server1" }
    }
  }
]



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

def make_public_cluster(clusters):
    new_cluster = {}
    for field in clusters:
        new_cluster[field]= clusters[field]
    return new_cluster

isCurrentNodeAdded = False

class ServerAPI(MethodView):

    def get(self, server_id):
        global isCurrentNodeAdded
        myhostname = socket.gethostname()
        myhostorip = socket.gethostbyname(myhostname)

        if server_id is None:

            if not servers and isCurrentNodeAdded==False:
                #add default server
                isCurrentNodeAdded = True
                servers.append(
                    {
                        'id': 1,
                        'name': myhostname,
                        'hostname': myhostorip,
                        'description': "",
                        'enabled': True,
                        'external-interface': "",
                        'internal-interface': "",
                        'public-interface':"",
                        "client-listener":"",
                        "internal-listener":"",
                        "admin-listener":"",
                        "http-listener":"",
                        "replication-listener":"",
                        "zookeeper-listener":"",
                        "placement-group":""
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

        if 'admin-listener' in request.json:
            if(request.json['admin-listener']!=""):
                if(":" in request.json['admin-listener']):
                    count =  request.json['admin-listener'].count(":")
                    if(count>1):
                       return make_response(jsonify({'error': 'Invalid admin listener'}), 404)
                    #validate both ip as well as port
                    array =  request.json['admin-listener'].split(":")
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
                        val = int(request.json['admin-listener'])
                        if val<0:
                            return make_response(jsonify({'error': 'Admin Listener must be a positive number'}), 404)
                        elif val<1 or val>65536:
                            return make_response(jsonify({'error': 'Admin Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Admin Listener must be a positive number'}), 404)

        if 'internal-listener' in request.json:
            if(request.json['internal-listener']!=""):
                if(":" in request.json['internal-listener']):
                    count =  request.json['internal-listener'].count(":")
                    if(count>1):
                       return make_response(jsonify({'error': 'Invalid internal listener'}), 404)
                    #validate both ip as well as port
                    array =  request.json['internal-listener'].split(":")
                    try:
                        socket.inet_aton(array[0])
                    # legal
                    except socket.error:
                        return make_response(jsonify({'error': 'Invalid IP address'}), 404)

                    #validate port only
                    try:
                        val = int(array[1])
                        if val<0:
                            return make_response(jsonify({'error': 'Internal Listener must be a positive number'}), 404)
                        elif val<1 or val>=65535:
                            return make_response(jsonify({'error': 'Internal Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Internal Listener must be a positive number'}), 404)

                else:
                    try:
                        val = int(request.json['internal-listener'])
                        if val<0:
                            return make_response(jsonify({'error': 'Internal Listener must be a positive number'}), 404)
                        elif val<1 or val>65536:
                            return make_response(jsonify({'error': 'Internal Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Internal Listener must be a positive number'}), 404)

        if 'http-listener' in request.json:
            if(request.json['http-listener']!=""):
                if(":" in request.json['http-listener']):
                    count =  request.json['http-listener'].count(":")
                    if(count>1):
                       return make_response(jsonify({'error': 'Invalid http listener'}), 404)
                    #validate both ip as well as port
                    array =  request.json['http-listener'].split(":")
                    try:
                        socket.inet_aton(array[0])
                    # legal
                    except socket.error:
                        return make_response(jsonify({'error': 'Invalid IP address'}), 404)

                    #validate port only
                    try:
                        val = int(array[1])
                        if val<0:
                            return make_response(jsonify({'error': 'Http Listener must be a positive number'}), 404)
                        elif val<1 or val>=65535:
                            return make_response(jsonify({'error': 'Http Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Http Listener must be a positive number'}), 404)

                else:
                    try:
                        val = int(request.json['http-listener'])
                        if val<0:
                            return make_response(jsonify({'error': 'Http Listener must be a positive number'}), 404)
                        elif val<1 or val>65536:
                            return make_response(jsonify({'error': 'Http Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Http Listener must be a positive number'}), 404)

        if 'zookeeper-listener' in request.json:
            if(request.json['zookeeper-listener']!=""):
                if(":" in request.json['zookeeper-listener']):
                    count =  request.json['zookeeper-listener'].count(":")
                    if(count>1):
                       return make_response(jsonify({'error': 'Invalid Zookeeper listener'}), 404)
                    #validate both ip as well as port
                    array =  request.json['zookeeper-listener'].split(":")
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
                        val = int(request.json['zookeeper-listener'])
                        if val<0:
                            return make_response(jsonify({'error': 'Zookeeper Listener must be a positive number'}), 404)
                        elif val<1 or val>65536:
                            return make_response(jsonify({'error': 'Zookeeper Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Zookeeper Listener must be a positive number'}), 404)

        if 'replication-listener' in request.json:
            if(request.json['replication-listener']!=""):
                if(":" in request.json['replication-listener']):
                    count =  request.json['replication-listener'].count(":")
                    if(count>1):
                       return make_response(jsonify({'error': 'Invalid Replicationlistener'}), 404)
                    #validate both ip as well as port
                    array =  request.json['replication-listener'].split(":")
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
                        val = int(request.json['replication-listener'])
                        if val<0:
                            return make_response(jsonify({'error': 'Replication Listener must be a positive number'}), 404)
                        elif val<1 or val>65536:
                            return make_response(jsonify({'error': 'Replication Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Replication Listener must be a positive number'}), 404)

        if 'client-listener' in request.json:
            if(request.json['client-listener']!=""):
                if(":" in request.json['client-listener']):
                    count =  request.json['client-listener'].count(":")
                    if(count>1):
                       return make_response(jsonify({'error': 'Invalid Client listener'}), 404)
                    #validate both ip as well as port
                    array =  request.json['client-listener'].split(":")
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
                        val = int(request.json['client-listener'])
                        if val<0:
                            return make_response(jsonify({'error': 'Client Listener must be a positive number'}), 404)
                        elif val<1 or val>65536:
                            return make_response(jsonify({'error': 'Client Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Client Listener must be a positive number'}), 404)

        if 'internal-interface' in request.json:
            if (request.json['internal-interface']!=""):
                try:
                    print "test" + str(request.json['internal-interface'])
                    socket.inet_aton(request.json['internal-interface'])
                except socket.error:
                    return make_response(jsonify({'error': 'Invalid IP address'}), 404)

        if 'external-interface' in request.json:
            if (request.json['external-interface']!=""):
                try:
                    socket.inet_aton(request.json['external-interface'])
                except socket.error:
                    return make_response(jsonify({'error': 'Invalid IP address'}), 404)

        if 'public-interface' in request.json:
            if (request.json['public-interface']!=""):
                try:
                    socket.inet_aton(request.json['public-interface'])
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
        'admin-listener': request.json.get('admin-listener',""),
        'zookeeper-listener': request.json.get('zookeeper-listener',""),
        'replication-listener': request.json.get('replication-listener',""),
        'client-listener': request.json.get('client-listener',""),
        'internal-interface': request.json.get('internal-interface',""),
        'external-interface': request.json.get('external-interface',""),
        'public-interface': request.json.get('public-interface',""),
        'internal-listener': request.json.get('internal-listener',""),
        'http-listener': request.json.get('http-listener',""),
        "placement-group": request.json.get('placement-group',""),

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

        if 'admin-listener' in request.json:
            if(request.json['admin-listener']!=""):
                if(":" in request.json['admin-listener']):
                    count =  request.json['admin-listener'].count(":")
                    print "test" + str(count)
                    if(count>1):
                       return make_response(jsonify({'error': 'Invalid admin listener'}), 404)
                    #validate both ip as well as port
                    array =  request.json['admin-listener'].split(":")
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
                        val = int(request.json['admin-listener'])
                        if val<0:
                            return make_response(jsonify({'error': 'Admin Listener must be a positive number'}), 404)
                        elif val<1 or val>65536:
                            return make_response(jsonify({'error': 'Admin Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Admin Listener must be a positive number'}), 404)


        if 'internal-listener' in request.json:
            if(request.json['internal-listener']!=""):
                if(":" in request.json['internal-listener']):
                    count =  request.json['internal-listener'].count(":")
                    if(count>1):
                       return make_response(jsonify({'error': 'Invalid internal listener'}), 404)
                    #validate both ip as well as port
                    array =  request.json['internal-listener'].split(":")
                    try:
                        socket.inet_aton(array[0])
                    # legal
                    except socket.error:
                        return make_response(jsonify({'error': 'Invalid IP address'}), 404)

                    #validate port only
                    try:
                        val = int(array[1])
                        if val<0:
                            return make_response(jsonify({'error': 'Internal Listener must be a positive number'}), 404)
                        elif val<1 or val>=65535:
                            return make_response(jsonify({'error': 'Internal Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Internal Listener must be a positive number'}), 404)

                else:
                    try:
                        val = int(request.json['internal-listener'])
                        if val<0:
                            return make_response(jsonify({'error': 'Internal Listener must be a positive number'}), 404)
                        elif val<1 or val>65536:
                            return make_response(jsonify({'error': 'Internal Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Internal Listener must be a positive number'}), 404)

        if 'http-listener' in request.json:
            if(request.json['http-listener']!=""):
                if(":" in request.json['http-listener']):
                    count =  request.json['http-listener'].count(":")
                    if(count>1):
                       return make_response(jsonify({'error': 'Invalid http listener'}), 404)
                    #validate both ip as well as port
                    array =  request.json['http-listener'].split(":")
                    try:
                        socket.inet_aton(array[0])
                    # legal
                    except socket.error:
                        return make_response(jsonify({'error': 'Invalid IP address'}), 404)

                    #validate port only
                    try:
                        val = int(array[1])
                        if val<0:
                            return make_response(jsonify({'error': 'Http Listener must be a positive number'}), 404)
                        elif val<1 or val>=65535:
                            return make_response(jsonify({'error': 'Http Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Http Listener must be a positive number'}), 404)

                else:
                    try:
                        val = int(request.json['http-listener'])
                        if val<0:
                            return make_response(jsonify({'error': 'Http Listener must be a positive number'}), 404)
                        elif val<1 or val>65536:
                            return make_response(jsonify({'error': 'Http Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Http Listener must be a positive number'}), 404)

        if 'zookeeper-listener' in request.json:
            if(request.json['zookeeper-listener']!=""):
                if(":" in request.json['zookeeper-listener']):
                    count =  request.json['zookeeper-listener'].count(":")
                    print "test" + str(count)
                    if(count>1):
                       return make_response(jsonify({'error': 'Invalid Zookeeper listener'}), 404)
                    #validate both ip as well as port
                    array =  request.json['zookeeper-listener'].split(":")
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
                        val = int(request.json['zookeeper-listener'])
                        if val<0:
                            return make_response(jsonify({'error': 'Zookeeper Listener must be a positive number'}), 404)
                        elif val<1 or val>65536:
                            return make_response(jsonify({'error': 'Zookeeper Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Zookeeper Listener must be a positive number'}), 404)

        if 'replication-listener' in request.json:
            if(request.json['replication-listener']!=""):
                if(":" in request.json['replication-listener']):
                    count =  request.json['replication-listener'].count(":")
                    if(count>1):
                       return make_response(jsonify({'error': 'Invalid Replicationlistener'}), 404)
                    #validate both ip as well as port
                    array =  request.json['replication-listener'].split(":")
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
                        val = int(request.json['replication-listener'])
                        if val<0:
                            return make_response(jsonify({'error': 'Replication Listener must be a positive number'}), 404)
                        elif val<1 or val>65536:
                            return make_response(jsonify({'error': 'Replication Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Replication Listener must be a positive number'}), 404)

        if 'client-listener' in request.json:
            if(request.json['client-listener']!=""):
                if(":" in request.json['client-listener']):
                    count =  request.json['client-listener'].count(":")
                    if(count>1):
                       return make_response(jsonify({'error': 'Invalid Client listener'}), 404)
                    #validate both ip as well as port
                    array =  request.json['client-listener'].split(":")
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
                        val = int(request.json['client-listener'])
                        if val<0:
                            return make_response(jsonify({'error': 'Client Listener must be a positive number'}), 404)
                        elif val<1 or val>65536:
                            return make_response(jsonify({'error': 'Client Listener must be greater than 1 and less than 65535'}), 404)
                    except ValueError:
                        return make_response(jsonify({'error': 'Client Listener must be a positive number'}), 404)

        if 'internal-interface' in request.json:
            if (request.json['internal-interface']!=""):
                try:
                    socket.inet_aton(request.json['internal-interface'])
                    # legal
                except socket.error:
                    return make_response(jsonify({'error': 'Invalid IP address'}), 404)

        if 'external-interface' in request.json:
            if (request.json['external-interface']!=""):
                try:
                    socket.inet_aton(request.json['external-interface'])
                    # legal
                except socket.error:
                    return make_response(jsonify({'error': 'Invalid IP address'}), 404)

        if 'public-interface' in request.json:
            if (request.json['public-interface']!=""):
                try:
                    socket.inet_aton(request.json['public-interface'])
                except socket.error:
                    return make_response(jsonify({'error': 'Invalid IP address'}), 404)

        currentserver[0]['name'] = request.json.get('name', currentserver[0]['name'])
        currentserver[0]['hostname'] = request.json.get('hostname', currentserver[0]['hostname'])
        currentserver[0]['description'] = request.json.get('description', currentserver[0]['description'])
        currentserver[0]['enabled'] = request.json.get('enabled', currentserver[0]['enabled'])
        currentserver[0]['admin-listener'] = request.json.get('admin-listener', currentserver[0]['admin-listener'])
        currentserver[0]['internal-listener'] = request.json.get('internal-listener', currentserver[0]['internal-listener'])
        currentserver[0]['http-listener'] = request.json.get('http-listener', currentserver[0]['http-listener'])
        currentserver[0]['zookeeper-listener'] = request.json.get('zookeeper-listener', currentserver[0]['zookeeper-listener'])
        currentserver[0]['replication-listener'] = request.json.get('replication-listener', currentserver[0]['replication-listener'])
        currentserver[0]['client-listener'] = request.json.get('client-listener', currentserver[0]['client-listener'])
        currentserver[0]['internal-interface'] = request.json.get('internal-interface', currentserver[0]['internal-interface'])
        currentserver[0]['external-interface'] = request.json.get('external-interface', currentserver[0]['external-interface'])
        currentserver[0]['public-interface'] = request.json.get('public-interface', currentserver[0]['public-interface'])
        currentserver[0]['placement-group'] = request.json.get('placement-group', currentserver[0]['placement-group'])
        return jsonify( { 'server': currentserver[0], 'status': 1} )

class ClusterAPI(MethodView):
    def get (self,cluster_id):
        global isCurrentNodeAdded

        if cluster_id is None:

            if not clusters and isCurrentNodeAdded==False:
                #add default server
                isCurrentNodeAdded = True
                clusters.append(
                    {
                        'id': 1,
                        'name': "cluster1",
                        'deployment': "default",
                        "members": {
                                "id": 1,
                                "member": { "name": "server1" }
                            }
                    }
                    )

            # return a list of users
            return jsonify( { 'clusters': map(make_public_cluster, clusters) } )
        else:
            # expose a single user
            cluster = filter(lambda t: t['id'] == cluster_id, clusters)
            if len(cluster) == 0:
                abort(404)
            return jsonify( { 'server': make_public_cluster(cluster[0]) } )


if __name__ == '__main__':
    app.config.update(
        DEBUG=True,
    );
    server_view = ServerAPI.as_view('server_api')
    cluster_view = ClusterAPI.as_view('cluster_api')
    app.add_url_rule('/api/1.0/servers/', defaults={'server_id': None},
                     view_func=server_view, methods=['GET',])
    app.add_url_rule('/api/1.0/servers/', view_func=server_view, methods=['POST',])
    app.add_url_rule('/api/1.0/servers/<int:server_id>', view_func=server_view,
                     methods=['GET', 'PUT', 'DELETE'])

    app.add_url_rule('/api/1.0/cluster/', defaults={'cluster_id': None},
                     view_func=cluster_view, methods=['GET',])
    app.add_url_rule('/api/1.0/cluster/<int:cluster_id>', view_func=cluster_view,
                     methods=['GET','PUT', 'DELETE'])
    app.add_url_rule('/api/1.0/cluster/', view_func=cluster_view, methods=['POST',])
    app.add_url_rule('/api/1.0/cluster/member', view_func=cluster_view,
                     methods=['POST',])
    app.add_url_rule('/api/1.0/cluster/member/<int:member_id>', view_func=cluster_view,
                     methods=['GET', 'PUT', 'DELETE'])


    app.run(threaded=True, host='0.0.0.0', port=8000)
