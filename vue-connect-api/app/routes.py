from app import app
from flask import jsonify
from flask import request
import requests
import json
import os
from datetime import datetime
from requests.exceptions import ConnectionError
from requests.exceptions import Timeout

# TODO make settimsg dynamic
DEFAULT_REST_ENDPOINT = 'http://localhost:8083'
DEFAULT_REQUEST_TIMEOUT_SEC = 5

ERROR_MSG_CLUSTER_NOT_REACHABLE = "Cluster {} not reachable!"
ERROR_MSG_CLUSTER_TIMEOUT = "Request timeout cluster {} was not reachable!"
ERROR_MSG_NOT_FOUND = "Resource not found."
ERROR_MSG_NOT_ALLOWED = "The method is not allowed for this resource."
ERROR_MSG_INTERNAL_SERVER_ERROR = "Internal server error."
ERROR_MSG_NO_DATA = "Missing data. {}."


def get_url():
    if os.getenv("CONNECT_URL") is not None:
        return os.getenv("CONNECT_URL")
    else:
        return DEFAULT_REST_ENDPOINT


@app.route('/api/connectors', strict_slashes=False, methods=['POST'])
def new():
    try:
        data = request.get_json()

        if data is None:
            return jsonify({'message': ERROR_MSG_NO_DATA.format('There was no connector configuration provided')}), 400

        if 'name' in data:
            name = data['name']
            del data['name']

            cfg = {'name': name, 'config': data}

            r = requests.post(get_url() + '/connectors/',
                              json=cfg, timeout=DEFAULT_REQUEST_TIMEOUT_SEC)
            status = r.json()

            return jsonify(status), r.status_code
        else:
            return jsonify({'message': 'Missing configuration property \'name\'.'}), 400

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLUSTER_NOT_REACHABLE.format(get_url())}), 400
    except Timeout:
        return jsonify({'message': ERROR_MSG_CLUSTER_TIMEOUT.format(get_url())}), 408

@app.route('/api/connectors/<id>/config', strict_slashes=False, methods=['POST'])
def update(id):
    try:
        data = request.get_json()

        if data is None:
            return jsonify({'message': ERROR_MSG_NO_DATA.format('There is no connector configuration for \'' + id + '\'')}), 400

        r = requests.put(get_url() + '/connectors/' +
                         id + '/config', json=data, timeout=DEFAULT_REQUEST_TIMEOUT_SEC)
        status = r.json()

        return jsonify(status), r.status_code

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLUSTER_NOT_REACHABLE.format(get_url())}), 400
    except Timeout:
        return jsonify({'message': ERROR_MSG_CLUSTER_TIMEOUT.format(get_url())}), 408


@app.route('/api/connectors/<id>/restart', strict_slashes=False, methods=['POST'])
def restart(id):
    try:
        requests.post(get_url() + '/connectors/' + id +
                      '/restart', timeout=DEFAULT_REQUEST_TIMEOUT_SEC)
        return connectors()

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLUSTER_NOT_REACHABLE.format(get_url())}), 400
    except Timeout:
        return jsonify({'message': ERROR_MSG_CLUSTER_TIMEOUT.format(get_url())}), 408

@app.route('/api/connectors/<id>/delete', strict_slashes=False, methods=['POST'])
def delete(id):
    try:
        requests.delete(get_url() + '/connectors/' + id,
                        timeout=DEFAULT_REQUEST_TIMEOUT_SEC)
        return connectors()

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLUSTER_NOT_REACHABLE.format(get_url())}), 400
    except Timeout:
        return jsonify({'message': ERROR_MSG_CLUSTER_TIMEOUT.format(get_url())}), 408

@app.route('/api/connectors/<id>/pause', strict_slashes=False, methods=['POST'])
def pause(id):
    try:
        requests.put(get_url() + '/connectors/' + id + '/pause',
                     timeout=DEFAULT_REQUEST_TIMEOUT_SEC)
        return connectors()

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLUSTER_NOT_REACHABLE.format(get_url())}), 400
    except Timeout:
        return jsonify({'message': ERROR_MSG_CLUSTER_TIMEOUT.format(get_url())}), 408

@app.route('/api/connectors/<id>/resume', strict_slashes=False, methods=['POST'])
def resume(id):
    try:
        requests.put(get_url() + '/connectors/' + id + '/resume',
                     timeout=DEFAULT_REQUEST_TIMEOUT_SEC)
        return connectors()

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLUSTER_NOT_REACHABLE.format(get_url())}), 400
    except Timeout:
        return jsonify({'message': ERROR_MSG_CLUSTER_TIMEOUT.format(get_url())}), 408

@app.route('/api/connectors/<id>/tasks/<task_id>/restart', strict_slashes=False, methods=['POST'])
def task_restart(id, task_id):
    try:
        requests.post(get_url() + '/connectors/' + id +
                      '/tasks/' + task_id + '/restart', timeout=DEFAULT_REQUEST_TIMEOUT_SEC)
        return connectors()

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLUSTER_NOT_REACHABLE.format(get_url())}), 400
    except Timeout:
        return jsonify({'message': ERROR_MSG_CLUSTER_TIMEOUT.format(get_url())}), 408

@app.route('/api/config/<id>', strict_slashes=False)
def config(id):
    try:
        r = requests.get(get_url() + '/connectors/' + id +
                         '/config', timeout=DEFAULT_REQUEST_TIMEOUT_SEC)
        config = r.json()
        return jsonify(config)

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLUSTER_NOT_REACHABLE.format(get_url())}), 400
    except Timeout:
        return jsonify({'message': ERROR_MSG_CLUSTER_TIMEOUT.format(get_url())}), 408

@app.route('/api/status', strict_slashes=False)
def connectors():
    try:

        state = []
        r = requests.get(get_url() + '/connectors?expand=info&expand=status',
                         timeout=DEFAULT_REQUEST_TIMEOUT_SEC)
        connectors = r.json()

        for name in connectors:
            connector = connectors[name]
                        
            connectorState = connector['status']
            if 'trace' in connectorState['connector']:
                connectorState['connector']['traceShort'] = connectorState['connector']['trace'].split('\n')[0]
                connectorState['connector']['traceException'] = connectorState['connector']['trace'].split(':')[0]

            for task in connectorState['tasks']:
                if 'trace' in task:
                   task['traceShort'] = task['trace'].split('\n')[0]
                   task['traceException'] = task['trace'].split(':')[0]

            
            state.append(connectorState)

        return jsonify(state)

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLUSTER_NOT_REACHABLE.format(get_url())}), 400
    except Timeout:
        return jsonify({'message': ERROR_MSG_CLUSTER_TIMEOUT.format(get_url())}), 408

@app.route('/api/status/<id>', strict_slashes=False)
def status(id):
    try:
        r = requests.get(get_url() + '/connectors/' + id +
                         '/status', timeout=DEFAULT_REQUEST_TIMEOUT_SEC)

        status = r.json()
        return jsonify(status), r.status_code

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLUSTER_NOT_REACHABLE.format(get_url())}), 400
    except Timeout:
        return jsonify({'message': ERROR_MSG_CLUSTER_TIMEOUT.format(get_url())}), 408

@app.route('/api/plugins/<name>/config/validate', strict_slashes=False, methods=['POST'])
def validate(name):
    try:
        data = request.get_json()
        if data is None:
            return jsonify({'message': ERROR_MSG_NO_DATA.format('connector configuration')}), 400

        r = requests.put(get_url() + '/connector-plugins/' +
                         name + '/config/validate', json=data, timeout=DEFAULT_REQUEST_TIMEOUT_SEC)
        config = r.json()

        return jsonify(config), r.status_code

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLUSTER_NOT_REACHABLE.format(get_url())}), 400
    except Timeout:
        return jsonify({'message': ERROR_MSG_CLUSTER_TIMEOUT.format(get_url())}), 408

@app.route('/api/plugins', strict_slashes=False)
def plugins():
    try:

        r = requests.get(get_url() + '/connector-plugins',
                         timeout=DEFAULT_REQUEST_TIMEOUT_SEC)
        plugins = r.json()

        for plugin in plugins:
            plugin['name'] = plugin['class'].split('.')[-1]

            # replace string null with None
            if plugin['version'] == 'null':
                plugin['version'] = None

        return jsonify(plugins)

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLUSTER_NOT_REACHABLE.format(get_url())}), 400
    except Timeout:
        return jsonify({'message': ERROR_MSG_CLUSTER_TIMEOUT.format(get_url())}), 408

@app.route('/api/info', strict_slashes=False)
def info():
    try:
        r = requests.get(get_url(), timeout=DEFAULT_REQUEST_TIMEOUT_SEC)

        info = r.json()
        info['last_update'] = datetime.now()
        info['endpoint'] = get_url()
        return jsonify(info)
    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLUSTER_NOT_REACHABLE.format(get_url())}), 400
    except Timeout:
        return jsonify({'message': ERROR_MSG_CLUSTER_TIMEOUT.format(get_url())}), 408

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
