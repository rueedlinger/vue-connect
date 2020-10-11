from app import app
from flask import jsonify
from flask import request
import requests
import json
import os
from datetime import datetime
from requests.exceptions import ConnectionError


DEFAULT_REST_ENDPOINT = 'http://localhost:8083'
ERROR_MSG_CLSUTER_NOT_REACHABLE = "Cluster {} not reachable!"
ERROR_MSG_NOT_FOUND = "Resource not found."
ERROR_MSG_NOT_ALLOWED = "The method is not allowed for this resource."
ERROR_MSG_INTERNAL_SERVER_ERROR = "Internal server error."
ERROR_MSG_NO_DATA = "Missing data. {}."

def get_url(): 
    if os.getenv("CONNECT_URL") is not None:
        return os.getenv("CONNECT_URL")
    else:
        return DEFAULT_REST_ENDPOINT



@app.route('/api/connectors', strict_slashes=False, methods = ['POST'])
def new():
    try:
        data = request.get_json()
        
        if data is None:
            return jsonify({'message': ERROR_MSG_NO_DATA.format('There was no connector configuration provided')}), 400

        if 'name' in data:
            name = data['name']
            del data['name']

            cfg = {'name': name, 'config': data}

            r = requests.post(get_url() + '/connectors/', json=cfg)
            status = r.json()
            
            return jsonify(status), r.status_code
        else:
            return jsonify({'message': 'Missing configuration property \'name\'.' }), 400
    
    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLSUTER_NOT_REACHABLE.format(get_url()) }), 400

@app.route('/api/connectors/<id>/config', strict_slashes=False, methods = ['POST'])
def update(id):
    try:
        data = request.get_json()

        if data is None:
            return jsonify({'message': ERROR_MSG_NO_DATA.format('There is no connector configuration for \'' + id + '\'')}), 400

        r = requests.put(get_url() + '/connectors/' + id + '/config', json=data)
        status = r.json()

        return jsonify(status), r.status_code

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLSUTER_NOT_REACHABLE.format(get_url()) }), 400

@app.route('/api/connectors/<id>/restart', strict_slashes=False, methods = ['POST'])
def restart(id):
    try:
        r = requests.post(get_url() + '/connectors/' + id + '/restart')
        return connectors()
    
    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLSUTER_NOT_REACHABLE.format(get_url()) }), 400

@app.route('/api/connectors/<id>/delete', strict_slashes=False, methods = ['POST'])
def delete(id):
    try:
        r = requests.delete(get_url() + '/connectors/' + id)
        return connectors()
    
    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLSUTER_NOT_REACHABLE.format(get_url()) }), 400

@app.route('/api/connectors/<id>/pause', strict_slashes=False, methods = ['POST'])
def pause(id):
    try:
        r = requests.put(get_url() + '/connectors/' + id + '/pause')
        return connectors()
    
    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLSUTER_NOT_REACHABLE.format(get_url()) }), 400

@app.route('/api/connectors/<id>/resume', strict_slashes=False, methods = ['POST'])
def resume(id):
    try:
        r = requests.put(get_url() + '/connectors/' + id + '/resume')
        return connectors()

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLSUTER_NOT_REACHABLE.format(get_url()) }), 400

@app.route('/api/connectors/<id>/tasks/<task_id>/restart', strict_slashes=False, methods = ['POST'])
def task_restart(id, task_id):
    try:
        r = requests.post(get_url() + '/connectors/' + id + '/tasks/' + task_id + '/restart')
        return connectors()
    
    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLSUTER_NOT_REACHABLE.format(get_url()) }), 400


@app.route('/api/config/<id>', strict_slashes=False)
def config(id):
    try:
        r = requests.get(get_url() + '/connectors/' + id + '/config')
        config = r.json()
        return jsonify(config)

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLSUTER_NOT_REACHABLE.format(get_url()) }), 400


@app.route('/api/status', strict_slashes=False)
def connectors():
    try:
        r = requests.get(get_url() + '/connectors')
        connectors = r.json()

        state = []

        for connector in connectors:
            r = requests.get(get_url() + '/connectors/' + connector + '/status')
            connector_status = r.json()
            connector_status['hash'] = hash(json.dumps(connector_status))
            state.append(connector_status)

        return jsonify(state)

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLSUTER_NOT_REACHABLE.format(get_url()) }), 400

@app.route('/api/status/<id>', strict_slashes=False)
def status(id):
    try:
        r = requests.get(get_url() + '/connectors/' + id + '/status')

        status = r.json()
        return jsonify(status), r.status_code

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLSUTER_NOT_REACHABLE.format(get_url()) }), 400


@app.route('/api/plugins/<name>/config/validate', strict_slashes=False, methods=['POST'])
def validate(name):
    try:
        data = request.get_json()
        if data is None:
            return jsonify({'message': ERROR_MSG_NO_DATA.format('connector configuration')}), 400

        r = requests.put(get_url() + '/connector-plugins/' + name + '/config/validate', json=data)
        config = r.json()

        return jsonify(config), r.status_code

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLSUTER_NOT_REACHABLE.format(get_url()) }), 400


@app.route('/api/plugins', strict_slashes=False)
def plugins():
    try:
        
        r = requests.get(get_url() + '/connector-plugins')
        plugins = r.json()

        for plugin in plugins:
            plugin['name'] = plugin['class'].split('.')[-1]

            # replace string null with None
            if plugin['version'] == 'null':
                plugin['version'] = None

        return jsonify(plugins)

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLSUTER_NOT_REACHABLE.format(get_url()) }), 400

@app.route('/api/info', strict_slashes=False)
def info():
    try:
        #LOGGER.info("info ddd")
        r = requests.get(get_url())

        info = r.json()
        info['last_update'] = datetime.now()
        info['endpoint'] = get_url()
        return jsonify(info)
    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLSUTER_NOT_REACHABLE.format(get_url()) }), 400

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'message': ERROR_MSG_NOT_FOUND}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'message': ERROR_MSG_NOT_ALLOWED}), 405

@app.errorhandler(500)
def internal_error(e):
    # TODO: log error
    return jsonify({'message': ERROR_MSG_INTERNAL_SERVER_ERROR}), 500
