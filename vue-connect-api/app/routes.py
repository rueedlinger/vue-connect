from app import app
from app import util

from flask import jsonify
from flask import request
from datetime import datetime
from requests.exceptions import ConnectionError
from requests.exceptions import Timeout
from apscheduler.schedulers.background import BackgroundScheduler

import time
import logging
import requests

ERROR_MSG_CLUSTER_NOT_REACHABLE = "Cluster {} not reachable!"
ERROR_MSG_CLUSTER_TIMEOUT = "Request timeout cluster {} was not reachable!"
ERROR_MSG_NOT_FOUND = "Resource not found."
ERROR_MSG_NOT_ALLOWED = "The method is not allowed for this resource."
ERROR_MSG_INTERNAL_SERVER_ERROR = "Internal server error."
ERROR_MSG_NO_DATA = "Missing data. {}."


cache = {
    'loadtime': 0,
    'state': None,
    'isConnectUp': False,
    'message': None
}

request_timeout_sec = util.get_request_timeout()
poll_intervall_sec = util.get_poll_intervall()
connect_url = util.get_url()


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

            r = requests.post(connect_url + '/connectors/',
                              json=cfg, timeout=request_timeout_sec)
            status = r.json()

            return jsonify(status), r.status_code
        else:
            return jsonify({'message': 'Missing configuration property \'name\'.'}), 400

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLUSTER_NOT_REACHABLE.format(connect_url)}), 503
    except Timeout:
        return jsonify({'message': ERROR_MSG_CLUSTER_TIMEOUT.format(connect_url)}), 504


@app.route('/api/connectors/<id>/config', strict_slashes=False, methods=['POST'])
def update(id):
    try:
        data = request.get_json()

        if data is None:
            return jsonify({'message': ERROR_MSG_NO_DATA.format('There is no connector configuration for \'' + id + '\'')}), 400

        r = requests.put(connect_url + '/connectors/' +
                         id + '/config', json=data, timeout=request_timeout_sec)
        status = r.json()

        return jsonify(status), r.status_code

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLUSTER_NOT_REACHABLE.format(connect_url)}), 503
    except Timeout:
        return jsonify({'message': ERROR_MSG_CLUSTER_TIMEOUT.format(connect_url)}), 504


@app.route('/api/connectors/<id>/restart', strict_slashes=False, methods=['POST'])
def restart(id):
    try:
        requests.post(connect_url + '/connectors/' + id +
                      '/restart', timeout=request_timeout_sec)
        return connectors()

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLUSTER_NOT_REACHABLE.format(connect_url)}), 503
    except Timeout:
        return jsonify({'message': ERROR_MSG_CLUSTER_TIMEOUT.format(connect_url)}), 504


@app.route('/api/connectors/<id>/delete', strict_slashes=False, methods=['POST'])
def delete(id):
    try:
        requests.delete(connect_url + '/connectors/' + id,
                        timeout=request_timeout_sec)
        return connectors()

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLUSTER_NOT_REACHABLE.format(connect_url)}), 503
    except Timeout:
        return jsonify({'message': ERROR_MSG_CLUSTER_TIMEOUT.format(connect_url)}), 504


@app.route('/api/connectors/<id>/pause', strict_slashes=False, methods=['POST'])
def pause(id):
    try:
        requests.put(connect_url + '/connectors/' + id + '/pause',
                     timeout=request_timeout_sec)
        return connectors()

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLUSTER_NOT_REACHABLE.format(connect_url)}), 503
    except Timeout:
        return jsonify({'message': ERROR_MSG_CLUSTER_TIMEOUT.format(connect_url)}), 504


@app.route('/api/connectors/<id>/resume', strict_slashes=False, methods=['POST'])
def resume(id):
    try:
        requests.put(connect_url + '/connectors/' + id + '/resume',
                     timeout=request_timeout_sec)
        return connectors()

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLUSTER_NOT_REACHABLE.format(connect_url)}), 503
    except Timeout:
        return jsonify({'message': ERROR_MSG_CLUSTER_TIMEOUT.format(connect_url)}), 504


@app.route('/api/connectors/<id>/tasks/<task_id>/restart', strict_slashes=False, methods=['POST'])
def task_restart(id, task_id):
    try:
        requests.post(connect_url + '/connectors/' + id +
                      '/tasks/' + task_id + '/restart', timeout=request_timeout_sec)
        return connectors()

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLUSTER_NOT_REACHABLE.format(connect_url)}), 503
    except Timeout:
        return jsonify({'message': ERROR_MSG_CLUSTER_TIMEOUT.format(connect_url)}), 504


@app.route('/api/config/<id>', strict_slashes=False)
def config(id):
    try:
        r = requests.get(connect_url + '/connectors/' + id +
                         '/config', timeout=request_timeout_sec)
        config = r.json()
        return jsonify(config)

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLUSTER_NOT_REACHABLE.format(connect_url)}), 503
    except Timeout:
        return jsonify({'message': ERROR_MSG_CLUSTER_TIMEOUT.format(connect_url)}), 504


@app.route('/api/polling', strict_slashes=False)
def polling():
    return jsonify(cache)


@app.route('/api/status', strict_slashes=False)
def connectors():
    try:
        state = load_state()
        update_cache(state)
        return jsonify(state)

    except ConnectionError:

        cache['message'] = ERROR_MSG_CLUSTER_NOT_REACHABLE.format(connect_url)
        cache['isConnectUp'] = False

        return jsonify({
            'message':  cache['message'],
            'cache': cache['state']
        }), 503
    except Timeout:

        cache['message'] = ERROR_MSG_CLUSTER_TIMEOUT.format(connect_url)
        cache['isConnectUp'] = False

        return jsonify({
            'message':  cache['message'],
            'cache': cache['state'],
        }), 504


def load_state():
    state = []
    r = requests.get(connect_url + '/connectors?expand=info&expand=status',
                     timeout=request_timeout_sec)
    connectors = r.json()
    for name in connectors:
        connector = connectors[name]
        connectorState = connector['status']

        if 'trace' in connectorState['connector']:
            trace_short_connector = connectorState['connector']['trace'].split(
                '\n')
            if len(trace_short_connector) > 0:
                connectorState['connector']['traceShort'] = trace_short_connector[0]

                short_task_connectors = trace_short_connector[0].split(':')

                if len(short_task_connectors) > 1:
                    connectorState['connector']['traceException'] = short_task_connectors[0].strip(
                    )
                    connectorState['connector']['traceMessage'] = short_task_connectors[1].strip(
                    )

        for task in connectorState['tasks']:
            if 'trace' in task:
                trace_short_task = task['trace'].split('\n')
                if len(trace_short_task) > 0:
                    task['traceShort'] = trace_short_task[0]

                    short_task_parts = trace_short_task[0].split(':')

                    if len(short_task_parts) > 1:
                        task['traceException'] = short_task_parts[0].strip()
                        task['traceMessage'] = short_task_parts[1].strip()

        state.append(connectorState)
    return state


@app.route('/api/status/<id>', strict_slashes=False)
def status(id):
    try:
        r = requests.get(connect_url + '/connectors/' + id +
                         '/status', timeout=request_timeout_sec)

        status = r.json()
        return jsonify(status), r.status_code

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLUSTER_NOT_REACHABLE.format(connect_url)}), 503
    except Timeout:
        return jsonify({'message': ERROR_MSG_CLUSTER_TIMEOUT.format(connect_url)}), 504


@app.route('/api/plugins/<name>/config/validate', strict_slashes=False, methods=['POST'])
def validate(name):
    try:
        data = request.get_json()
        if data is None:
            return jsonify({'message': ERROR_MSG_NO_DATA.format('connector configuration')}), 400

        r = requests.put(connect_url + '/connector-plugins/' +
                         name + '/config/validate', json=data, timeout=request_timeout_sec)
        config = r.json()

        return jsonify(config), r.status_code

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLUSTER_NOT_REACHABLE.format(connect_url)}), 503
    except Timeout:
        return jsonify({'message': ERROR_MSG_CLUSTER_TIMEOUT.format(connect_url)}), 504


@app.route('/api/plugins', strict_slashes=False)
def plugins():
    try:

        r = requests.get(connect_url + '/connector-plugins',
                         timeout=request_timeout_sec)
        plugins = r.json()

        for plugin in plugins:
            plugin['name'] = plugin['class'].split('.')[-1]

            # replace string null with None
            if plugin['version'] == 'null':
                plugin['version'] = None

        return jsonify(plugins)

    except ConnectionError:
        return jsonify({'message': ERROR_MSG_CLUSTER_NOT_REACHABLE.format(connect_url)}), 503
    except Timeout:
        return jsonify({'message': ERROR_MSG_CLUSTER_TIMEOUT.format(connect_url)}), 504


@app.route('/api/info', strict_slashes=False)
def info():

    app_info = {}
    app_info['endpoint'] = connect_url
    app_info['vc_version'] = util.get_str_config('VC_VERSION', 'dev')
    app_info['tags'] = util.get_str_config('VC_TAGS', None)
    app_info['sha'] = util.get_str_config('VC_IMAGE_GITHUB_SHA', None)
    app_info['build_time'] = util.get_str_config('VC_IMAGE_BUILD_TIME', None)

    try:
        r = requests.get(connect_url, timeout=request_timeout_sec)

        info = r.json()
        info.update(app_info)

        return jsonify(info)
    except ConnectionError:
        return jsonify({
            'message': ERROR_MSG_CLUSTER_NOT_REACHABLE.format(connect_url),
            'cache': app_info
        }), 503
    except Timeout:
        return jsonify({
            'message': ERROR_MSG_CLUSTER_TIMEOUT.format(connect_url),
            'cache': app_info
        }), 504


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'message': ERROR_MSG_NOT_FOUND}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'message': ERROR_MSG_NOT_ALLOWED}), 405


@app.errorhandler(500)
def internal_error(e):
    logging.error(e)
    return jsonify({'message': ERROR_MSG_INTERNAL_SERVER_ERROR}), 500


def update_cache(state):
    
    cache['state'] = state
    cache['loadtime'] = time.time()
    cache['isConnectUp'] = True
    cache['message'] = None


def job_update_cache():
    logging.info('updating cache')
    try:
        state = load_state()
        update_cache(state)
    except ConnectionError:
        cache['isConnectUp'] = False
        cache['message'] = ERROR_MSG_CLUSTER_NOT_REACHABLE.format(connect_url)
        logging.info(ERROR_MSG_CLUSTER_NOT_REACHABLE.format(connect_url))
    except Timeout:
        cache['message'] = ERROR_MSG_CLUSTER_TIMEOUT.format(connect_url)
        cache['isConnectUp'] = False
        logging.info(ERROR_MSG_CLUSTER_TIMEOUT.format(connect_url))
    except Exception as e:
        cache['isConnectUp'] = False
        cache['message'] = ERROR_MSG_INTERNAL_SERVER_ERROR
        logging.error('Could not update cache: %s', e)



if poll_intervall_sec > 0:
    job_update_cache()
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(func=job_update_cache, trigger="interval",
                      seconds=poll_intervall_sec)
    scheduler.start()
