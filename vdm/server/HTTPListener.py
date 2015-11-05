from flask import Flask, render_template, jsonify, abort, make_response, request
from flask.views import MethodView

app = Flask(__name__, template_folder ="../templates", static_folder="../static")

servers = [
    {
        'id': 1,
        'name': u'voltdb1',
        'hostname': u'voltdb1',
        'description': u'voltdb server 1',
        'enabled': True
    },
    {
        'id': 2,
        'name': u'voltdb2',
        'hostname': u'voltdb2',
        'description': u'voltdb server 2',
        'enabled': True
    },
    {
        'id': 3,
        'name': u'voltdb3',
        'hostname': u'voltdb3',
        'description': u'voltdb server 3',
        'enabled': True
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
        'enabled': True
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
        server = filter(lambda t: t['id'] == server_id, servers)
        if len(server) == 0:
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

        server[0]['name'] = request.json.get('name', server[0]['name'])
        server[0]['description'] = request.json.get('description', server[0]['description'])
        # server[0]['enabled'] = request.json.get('enabled', server[0]['enabled'])
        server[0]['hostname'] = request.json.get('hostname', server[0]['hostname'])
        return jsonify( { 'server': server[0], 'status':1 } )

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
