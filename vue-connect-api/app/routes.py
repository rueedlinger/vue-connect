from app import app
from flask import jsonify
import requests
import json
from datetime import datetime

REST_ENDPOINT = 'http://localhost:8083'


@app.route('/api/connectors/<id>/restart', methods = ['POST'])
def restart(id):
    r = requests.post(REST_ENDPOINT + '/connectors/' + id + '/restart')
    return connectors()

@app.route('/api/connectors/<id>/delete', methods = ['POST'])
def delete(id):
    r = requests.delete(REST_ENDPOINT + '/connectors/' + id)
    return connectors()

@app.route('/api/connectors/<id>/pause', methods = ['POST'])
def pause(id):
    r = requests.put(REST_ENDPOINT + '/connectors/' + id + '/pause')
    return connectors()

@app.route('/api/connectors/<id>/resume', methods = ['POST'])
def resume(id):
    r = requests.put(REST_ENDPOINT + '/connectors/' + id + '/resume')
    return connectors()

@app.route('/api/connectors/<id>/tasks/<task_id>/restart', methods = ['POST'])
def task_restart(id, task_id):
    r = requests.post(REST_ENDPOINT + '/connectors/' + id + '/tasks/' + task_id + '/restart')
    return connectors()


@app.route('/api/config/<id>')
def config(id):
    r = requests.get(REST_ENDPOINT + '/connectors/' + id + '/config')
    config = r.json()
    return jsonify(config)


@app.route('/api/status')
def connectors():
    r = requests.get(REST_ENDPOINT + '/connectors')
    connectors = r.json()

    state = []

    for connector in connectors:
        r = requests.get(REST_ENDPOINT + '/connectors/' + connector + '/status')
        state.append(r.json())

    return jsonify(state)

@app.route('/api/status/<id>')
def status(id):
    r = requests.get(REST_ENDPOINT + '/connectors/' + id + '/status')
    status = r.json()
    return jsonify(status)

@app.route('/api/plugins')
def plugins():
    r = requests.get(REST_ENDPOINT + '/connector-plugins')
    plugins = r.json()

    for plugin in plugins:
        plugin['name'] = plugin['class'].split('.')[-1]

        # replace string null with None
        if plugin['version'] == 'null':
            plugin['version'] = None

    return jsonify(plugins)

@app.route('/api/info')
def info():
    r = requests.get(REST_ENDPOINT)

    info = r.json()
    info['last_update'] = datetime.now()
    info['endpoint'] = REST_ENDPOINT
    return jsonify(info)