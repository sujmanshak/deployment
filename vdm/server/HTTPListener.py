from flask import Flask, render_template, jsonify, abort, make_response, request

app = Flask(__name__)

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

@app.route('/api/1.0/servers/', methods=['GET'])
def get_servers():
    return jsonify({'servers':servers})

@app.route('/api/1.0/servers/<int:serverId>', methods=['GET'])
def get_server(serverId):
    server = filter(lambda t: t['id'] == serverId, servers)
    if len(server) == 0:
        abort(404)
    return jsonify( { 'server': server[0] } )

@app.route('/api/1.0/servers/', methods=['POST'])
def create_server():
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
    return jsonify( { 'server': server } ),201

@app.route('/api/1.0/servers/<int:serverId>', methods=['PUT'])
def update_server(serverId):
    # update a single server
    server = filter(lambda t: t['id'] == serverId, servers)
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
    server[0]['name'] = request.json.get('name', server[0]['name'])
    server[0]['description'] = request.json.get('description', server[0]['description'])
    server[0]['enabled'] = request.json.get('enabled', server[0]['enabled'])
    return jsonify( { 'server': server[0] } )

@app.route('/api/1.0/servers/<int:serverId>', methods=['DELETE'])
def delete_server(serverId):
    # delete a single server
    server = filter(lambda t: t['id'] == serverId, servers)
    if len(server) == 0:
        abort(404)
    servers.remove(server[0])
    return jsonify( { 'result': True } )

if __name__ == '__main__':
    app.config.update(
        DEBUG=True,
    );
    app.run(debug=True, host='0.0.0.0', port=8000)
