#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.views import MethodView

app = Flask(__name__, static_url_path = "")
 
servers = [
    {
        'id': 1,
        'name': u'volt3g',
        'hostname': u'volt3g',
        'description': u'My volt3g', 
        'enabled': True
    },
    {
        'id': 2,
        'name': u'volt3h',
        'hostname': u'volt3h',
        'description': u'My volt3h', 
        'enabled': True
    },
    {
        'id': 3,
        'name': u'volt3i',
        'hostname': u'volt3i',
        'description': u'My volt3i', 
        'enabled': True
    }
]

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

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
        print self;
        # create a new user
        if not request.json or not 'name' in request.json or not 'hostname' in request.json:
            abort(400)
        server = {
            'id': servers[-1]['id'] + 1,
            'name': request.json['name'],
            'description': request.json.get('description', ""),
            'hostname': request.json.get('hostname', ""),
            'enabled': True
        }
        servers.append(server)
        return jsonify( { 'server': make_public_server(server) } ), 201

    def delete(self, server_id):
        # delete a single user
        server = filter(lambda t: t['id'] == server_id, servers)
        if len(server) == 0:
            abort(404)
        servers.remove(server['id'])
        return jsonify( { 'result': True } )

    def put(self, server_id):
        # update a single user
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
        server[0]['title'] = request.json.get('title', server[0]['title'])
        server[0]['description'] = request.json.get('description', server[0]['description'])
        server[0]['enabled'] = request.json.get('enabled', server[0]['enabled'])
        return jsonify( { 'server': make_public_server(server[0]) } )

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
    app.run(threaded=True, host='0.0.0.0', port=9999)
