from . import app, GET, PUT, POST, DELETE
from flask import request, jsonify
from typing import List, Tuple
import requests
from random import randint

data = []
STAY_ALIVE = 5

@app.route('/register')
def register():
    node_num = len(data)

    if data:
        host = data[randint(0, len(data)-1)]
    else:
        host = 0

    data.append(request.remote_addr)

    payload = {
        'num': request.remote_addr,
        'recommendation': host
    }

    return jsonify(payload)

@app.route('/map')
def map():
    netmap = {key: [] for key in data}
    for host, connections in netmap.items():
        r = requests.get(f'http://{host}:5000/map')
        connections.extend(r.json())

    return jsonify(netmap)


@app.route('/store/<key>/<message>')
def store(key, message):
    host = data[randint(0, len(data)-1)]

    r = requests.get(f'http://{host}:5000/store/{key}/{message}')

    return r.text, 200

@app.route('/retrieve/<key>')
def retrieve(key):
    host = data[randint(0, len(data)-1)]

    r = requests.get(f'http://{host}:5000/retrieve/{key}/{STAY_ALIVE}')

    return r.text, 200



@app.route('/info')
def info():
    return jsonify(data)
