from app import app
from flask import jsonify
from flask import request
import requests
import json
import os
#import logging
from datetime import datetime
from requests.exceptions import ConnectionError


DEFAULT_REST_ENDPOINT = 'http://localhost:8083'
ERROR_MSG_CLSUTER_NOT_REACHABLE = "Cluster {} not reachable!"

#LOGGER = logging.getLogger('whatever')


def get_url(): 
    if os.getenv("CONNECT_URL") is not None:
        return os.getenv("CONNECT_URL")
    else:
        return DEFAULT_REST_ENDPOINT



@app.route('/api/connectors/', methods = ['POST'])
def new():
    try:
        data = request.get_json()
        if 'name' in data:
            name = data['name']
            del data['name']

            cfg = {'name': name, 'config': data}

            r = requests.post(get_url() + '/connectors/', json=cfg)
            status = r.json()
            
            return jsonify(status), r.status_code
        else:
            return jsonify({'message': 'Missing configuration \'name\' -> Globally unique name to use for this connector.' }), 400
    
    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLSUTER_NOT_REACHABLE.format(get_url()) }), 400

@app.route('/api/connectors/<id>/config', methods = ['POST'])
def update(id):
    try:
        data = request.get_json()
        r = requests.put(get_url() + '/connectors/' + id + '/config', json=data)
        status = r.json()

        return jsonify(status), r.status_code

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLSUTER_NOT_REACHABLE.format(get_url()) }), 400

@app.route('/api/connectors/<id>/restart', methods = ['POST'])
def restart(id):
    try:
        r = requests.post(get_url() + '/connectors/' + id + '/restart')
        return connectors()
    
    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLSUTER_NOT_REACHABLE.format(get_url()) }), 400

@app.route('/api/connectors/<id>/delete', methods = ['POST'])
def delete(id):
    try:
        r = requests.delete(get_url() + '/connectors/' + id)
        return connectors()
    
    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLSUTER_NOT_REACHABLE.format(get_url()) }), 400

@app.route('/api/connectors/<id>/pause', methods = ['POST'])
def pause(id):
    try:
        r = requests.put(get_url() + '/connectors/' + id + '/pause')
        return connectors()
    
    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLSUTER_NOT_REACHABLE.format(get_url()) }), 400

@app.route('/api/connectors/<id>/resume', methods = ['POST'])
def resume(id):
    try:
        r = requests.put(get_url() + '/connectors/' + id + '/resume')
        return connectors()
    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLSUTER_NOT_REACHABLE.format(get_url()) }), 400

@app.route('/api/connectors/<id>/tasks/<task_id>/restart', methods = ['POST'])
def task_restart(id, task_id):
    try:
        r = requests.post(get_url() + '/connectors/' + id + '/tasks/' + task_id + '/restart')
        return connectors()
    
    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLSUTER_NOT_REACHABLE.format(get_url()) }), 400


@app.route('/api/config/<id>')
def config(id):
    try:
        r = requests.get(get_url() + '/connectors/' + id + '/config')
        config = r.json()
        return jsonify(config)

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLSUTER_NOT_REACHABLE.format(get_url()) }), 400


@app.route('/api/status')
def connectors():
    try:
        r = requests.get(get_url() + '/connectors')
        connectors = r.json()

        state = []

        for connector in connectors:
            r = requests.get(get_url() + '/connectors/' + connector + '/status')
            state.append(r.json())

        return jsonify(state)

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLSUTER_NOT_REACHABLE.format(get_url()) }), 400

@app.route('/api/status/<id>')
def status(id):
    r = requests.get(get_url() + '/connectors/' + id + '/status')
    status = r.json()
    return jsonify(status)

@app.route('/api/plugins/<name>/config/validate', methods=['POST'])
def validate(name):
    try:
        data = request.get_json()
        print(data)
        r = requests.put(get_url() + '/connector-plugins/' + name + '/config/validate', json=data)
        config = r.json()

        return jsonify(config), r.status_code

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLSUTER_NOT_REACHABLE.format(get_url()) }), 400


@app.route('/api/plugins')
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

@app.route('/api/info')
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