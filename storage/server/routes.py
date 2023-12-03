from . import app, GET, PUT, POST, DELETE
from flask import request, jsonify, redirect
from typing import List, Tuple
from json import loads
import requests

r = requests.get('http://proxy:5000/register')

myinfo = loads(r.text)

mynum = myinfo['num']

neighbors = {str(key):val for key, val in myinfo['neighbors']}
data = {}

def hash_str(string_in):
    return sum(ord(c) for c in string_in)

@app.route('/add_neighbor', methods=POST)
def register():
    
    neighbors.update(request.json)

    return 'OK',200

@app.route('/info')
def info():
    return jsonify(neighbors) + jsonify(data)

@app.route('/store/<key>/<message>')
@app.route('/store/<key>/<message>/<steps>')
def store(key, message, steps = 0):
    steps = int(steps) + 1
    hashbits = 1
    max_neighbor = max(int(val) for val in neighbors.keys())
    max_neighbor = max(mynum, max_neighbor)
    while hashbits < max_neighbor:
        hashbits = hashbits << 1
    hashbits -= 1

    hashval = hash_str(key) & hashbits

    if hashval == mynum:
        data[key] = message
        return f'Stored in {steps} steps', 200
    else:
        nextbit = 1
        while (nextbit & mynum) == (nextbit & hashval):
            nextbit <<= 1
        neighbor_num = str(mynum ^ nextbit)
        # return f"Hash value: {hashval}; {mynum} sending to {neighbor_num}"
        try:
            neighbor = neighbors[neighbor_num]
            print(f"Hash value: {hashval}; {mynum} sending to {neighbor_num}", flush=True)
            return redirect(f'http://{neighbor}:5000/store/{key}/{message}/{steps}')
        except Exception as e:
            print(e, flush=True)
            return str(neighbors), 404

@app.route('/retrieve/<key>')
@app.route('/retrieve/<key>/<steps>')
def retrieve(key, steps=0):
    steps = int(steps) + 1
    hashbits = 1
    max_neighbor = max(int(val) for val in neighbors.keys())
    max_neighbor = max(mynum, max_neighbor)
    while hashbits < max_neighbor:
        hashbits = hashbits << 1
    hashbits -= 1

    hashval = hash_str(key) & hashbits

    if hashval == mynum:
        if key in data:
            payload = {
                key: data[key],
                "steps": steps
            }
            code = 200
        else:
            payload = {
                "key": 0,
                "steps": steps
            }
            code = 404
        return payload, code
    else:
        nextbit = 1
        while (nextbit & mynum) == (nextbit & hashval):
            nextbit <<= 1
        neighbor_num = str(mynum ^ nextbit)
        # return f"Hash value: {hashval}; {mynum} sending to {neighbor_num}"
        try:
            neighbor = neighbors[neighbor_num]
            print(f"Hash value: {hashval}; {mynum} sending to {neighbor_num}", flush=True)
            return redirect(f'http://{neighbor}:5000/retrieve/{key}/{steps}')
        except Exception as e:
            print(e, flush=True)
            return str(neighbors), 404
