from . import app, GET, PUT, POST, DELETE
from flask import request, jsonify
from typing import List, Tuple
import requests
from random import randint

data = []

@app.route('/register')
def register():
    node_num = len(data)
    neighbors: List[List] = []
    print(node_num)

    i = 1
    while i <= node_num:
        candidate = i ^ node_num
        print(candidate)
        if candidate < node_num:
            neighbors.append([candidate, data[candidate]])
        i = i << 1

    for num, addr in neighbors:
        payload = {node_num: request.remote_addr}
        requests.post(f'http://{addr}:5000/add_neighbor', json=payload)


    data.append(request.remote_addr)

    payload = {
        'num': node_num,
        'neighbors': neighbors
    }

    return jsonify(payload)

@app.route('/store/<key>/<message>')
def store(key, message):
    host = data[randint(0, len(data)-1)]

    r = requests.get(f'http://{host}:5000/store/{key}/{message}')

    return r.text, 200

@app.route('/retrieve/<key>')
def retrieve(key):
    host = data[randint(0, len(data)-1)]

    r = requests.get(f'http://{host}:5000/retrieve/{key}')

    return r.text, 200



@app.route('/info')
def info():
    return jsonify(data)
