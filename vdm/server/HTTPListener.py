from flask import Flask, render_template, jsonify, abort, make_response, request
from flask.views import MethodView

app = Flask(__name__, template_folder ="../templates", static_folder="../static")

servers = [
    {
        'id': 1,
        'name': u'voltdb1',
        'hostname': u'voltdb1',
        'description': u'voltdb server 1',
        'enabled': True,
        'portname': '21223',
        'adminport': '21211',
        'http': '8080',
        'internalport':'3021',
        'zookeeper': '2181',
        'replicationport':'5555'
    },
    {
        'id': 2,
        'name': u'voltdb2',
        'hostname': u'voltdb2',
        'description': u'voltdb server 2',
        'enabled': True,
        'portname': '21223',
        'adminport': '21211',
        'http': '8080',
        'internalport':'3021',
        'zookeeper': '2181',
        'replicationport':'5555'
    },
    {
        'id': 3,
        'name': u'voltdb3',
        'hostname': u'voltdb3',
        'description': u'voltdb server 3',
        'enabled': True,
        'portname': '21223',
        'adminport': '21211',
        'http': '8080',
        'internalport':'3021',
        'zookeeper': '2181',
        'replicationport':'5555'
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


class ServerAPI(MethodView):

    def get(self, server_id):
        if server_id is None:
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

        if 'portname' in request.json:
            if(request.json['portname']!=""):
                try:
                    val = int(request.json['portname'])
                    if val<0:
                        return make_response(jsonify({'error': 'Port name must be a positive number'}), 404)
                    elif val<1 or val>65535:
                        return make_response(jsonify({'error': 'Port name must be greater than 1 and less than 65535'}), 404)
                except ValueError:
                        return make_response(jsonify({'error': 'Port name must be a positive number'}), 404)

        if 'adminport' in request.json:
            if(request.json['adminport']!=""):
                try:
                    val = int(request.json['adminport'])
                    if val<0:
                        return make_response(jsonify({'error': 'Admin port must be a positive number'}), 404)
                    elif val<1 or val>=65535:
                        return make_response(jsonify({'error': 'Admin port must be greater than 1 and less than 65535'}), 404)
                except ValueError:
                    return make_response(jsonify({'error': 'Admin port must be a positive number'}), 404)

        if 'http' in request.json:
            if(request.json['http']!=""):
                try:
                    val = int(request.json['http'])
                    if val<0:
                        return make_response(jsonify({'error': 'Http must be a positive number'}), 404)
                    elif val<1 or val>65535:
                        return make_response(jsonify({'error': 'Http must be greater than 1 and less than 65535'}), 404)
                except ValueError:
                    return make_response(jsonify({'error': 'Http must be a positive number'}), 404)

        if 'internalport' in request.json:
            if(request.json['internalport']!=""):
                try:
                    val = int(request.json['internalport'])
                    if val<0:
                        return make_response(jsonify({'error': 'Internal port must be a positive number'}), 404)
                    elif val<1 or val>65535:
                        return make_response(jsonify({'error': 'Internal port must be greater than 1 and less than 65535'}), 404)
                except ValueError:
                    return make_response(jsonify({'error': 'Internal port must be a positive number'}), 404)

        if 'zookeeper' in request.json:
            if(request.json['zookeeper']!=""):
                try:
                    val = int(request.json['zookeeper'])
                    if val<0:
                        return make_response(jsonify({'error': 'Zookeeper must be a positive number'}), 404)
                    elif val<1 or val>65535:
                        return make_response(jsonify({'error': 'Zookeeper must be greater than 1 and less than 65535'}), 404)
                except ValueError:
                    return make_response(jsonify({'error': 'Zookeeper must be a positive number'}), 404)

        if 'replicationport' in request.json:
            if(request.json['replicationport']!=""):
                try:
                    val = int(request.json['replicationport'])
                    if val<0:
                        return make_response(jsonify({'error': 'Replication port must be a positive number'}), 404)
                    elif val<1 or val>65535:
                        return make_response(jsonify({'error': 'Replication port must be greater than 1 and less than 65535'}), 404)
                except ValueError:
                    return make_response(jsonify({'error': 'Replication port must be a positive number'}), 404)



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
        'portname': request.json.get('portname',""),
        'adminport': request.json.get('adminport',""),
        'http': request.json.get('http',""),
        'internalport': request.json.get('internalport',""),
        'zookeeper': request.json.get('zookeeper',""),
        'replicationport': request.json.get('replicationport',"")
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
            server = filter(lambda t: t['name'] == request.json['name'], servers)
            if len(server)!=0:
                return make_response(jsonify({'error': 'Server name already exists'}), 404)

        if 'hostname' in request.json:
            if request.json['hostname']=="":
                return make_response(jsonify({'error':'Host name is required'}),404)
            server = filter(lambda t: t['hostname'] == request.json['hostname'], servers)
            if len(server)!=0:
                return make_response(jsonify({'error': 'Host name already exists'}), 404)

        if 'portname' in request.json:
            if(request.json['portname']!=""):
                try:
                    val = int(request.json['portname'])
                    if val<0:
                        return make_response(jsonify({'error': 'Port name must be a positive number'}), 404)
                    elif val<1 or val>65535:
                        return make_response(jsonify({'error': 'Port name must be greater than 1 and less than 65535'}), 404)
                except ValueError:
                        return make_response(jsonify({'error': 'Port name must be a positive number'}), 404)

        if 'adminport' in request.json:
            if(request.json['adminport']!=""):
                try:
                    val = int(request.json['adminport'])
                    if val<0:
                        return make_response(jsonify({'error': 'Admin port must be a positive number'}), 404)
                    elif val<1 or val>=65535:
                        return make_response(jsonify({'error': 'Admin port must be greater than 1 and less than 65535'}), 404)
                except ValueError:
                    return make_response(jsonify({'error': 'Admin port must be a positive number'}), 404)

        if 'http' in request.json:
            if(request.json['http']!=""):
                try:
                    val = int(request.json['http'])
                    if val<0:
                        return make_response(jsonify({'error': 'Http must be a positive number'}), 404)
                    elif val<1 or val>65535:
                        return make_response(jsonify({'error': 'Http must be greater than 1 and less than 65535'}), 404)
                except ValueError:
                    return make_response(jsonify({'error': 'Http must be a positive number'}), 404)

        if 'internalport' in request.json:
            if(request.json['internalport']!=""):
                try:
                    val = int(request.json['internalport'])
                    if val<0:
                        return make_response(jsonify({'error': 'Internal port must be a positive number'}), 404)
                    elif val<1 or val>65535:
                        return make_response(jsonify({'error': 'Internal port must be greater than 1 and less than 65535'}), 404)
                except ValueError:
                    return make_response(jsonify({'error': 'Internal port must be a positive number'}), 404)

        if 'zookeeper' in request.json:
            if(request.json['zookeeper']!=""):
                try:
                    val = int(request.json['zookeeper'])
                    if val<0:
                        return make_response(jsonify({'error': 'Zookeeper must be a positive number'}), 404)
                    elif val<1 or val>65535:
                        return make_response(jsonify({'error': 'Zookeeper must be greater than 1 and less than 65535'}), 404)
                except ValueError:
                    return make_response(jsonify({'error': 'Zookeeper must be a positive number'}), 404)

        if 'replicationport' in request.json:
            if(request.json['replicationport']!=""):
                try:
                    val = int(request.json['replicationport'])
                    if val<0:
                        return make_response(jsonify({'error': 'Replication port must be a positive number'}), 404)
                    elif val<1 or val>65535:
                        return make_response(jsonify({'error': 'Replication port must be greater than 1 and less than 65535'}), 404)
                except ValueError:
                    return make_response(jsonify({'error': 'Replication port must be a positive number'}), 404)

        currentserver[0]['name'] = request.json.get('name', currentserver[0]['name'])
        currentserver[0]['hostname'] = request.json.get('hostname', currentserver[0]['hostname'])
        currentserver[0]['description'] = request.json.get('description', currentserver[0]['description'])
        currentserver[0]['enabled'] = request.json.get('enabled', currentserver[0]['enabled'])
        currentserver[0]['portname'] = request.json.get('portname', currentserver[0]['portname'])
        currentserver[0]['adminport'] = request.json.get('adminport', currentserver[0]['adminport'])
        currentserver[0]['http'] = request.json.get('http', currentserver[0]['http'])
        currentserver[0]['internalport'] = request.json.get('internalport', currentserver[0]['internalport'])
        currentserver[0]['zookeeper'] = request.json.get('zookeeper', currentserver[0]['zookeeper'])
        currentserver[0]['replicationport'] = request.json.get('replicationport', currentserver[0]['replicationport'])
        return jsonify( { 'server': currentserver[0] } )


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
