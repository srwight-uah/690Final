from random import randint, random
from . import app, GET, PUT, POST, DELETE
from flask import request, jsonify, redirect
from typing import List, Tuple
from json import loads
import requests

STORE_LIKELIHOOD = 0.2

r = requests.get('http://r_proxy:5000/register')

myinfo = loads(r.text)

mynum = myinfo['num']
neighbors = []
already_asked = set()
recommendation = myinfo['recommendation']

while recommendation:
    if recommendation in neighbors:
        break
    print(f"befriending {recommendation}", flush=True)
    r = requests.get(f'http://{recommendation}:5000/make_friends/{len(neighbors)}')
    response = loads(r.text)
    if response['friend'] == True:
        neighbors.append(recommendation)
    recommendation = response['recommendation']

data = {}

@app.route('/make_friends/<mycount>', methods=GET)
def make_friends(mycount):

    friend = request.remote_addr
    mycount = int(mycount)
    payload = {
        "friend": False,
        "recommendation": 0
    }

    # We're already friends
    if friend in neighbors:
        return jsonify(payload)

    if neighbors:
        rec = neighbors[randint(0, len(neighbors)-1)]
    else:
        rec = 0

    # If you have more friend than me, then yes but I won't recommend
    if mycount > len(neighbors):
        payload['friend'] = True

        print(f"My count: {len(neighbors)} Their count: {mycount} Friends: {payload['friend']} Recommended: {payload['recommendation']}", flush=True)
        neighbors.append(friend)
        return jsonify(payload)
    
    # If I have more friends than you and it's your first time asking, then no but recommend
    if (len(neighbors) > mycount) and (friend not in already_asked):
        payload['recommendation'] = rec
        already_asked.add(friend)
        print(f"My count: {len(neighbors)} Their count: {mycount} Friends: {payload['friend']} Recommended: {payload['recommendation']}", flush=True)
        return jsonify(payload)

    # If I have more friends than you but you already asked, then yes and recommend
    if (len(neighbors) > mycount) and (friend in already_asked):
        already_asked.remove(friend)

        payload['friend'] = True
        payload['recommendation'] = rec

        print(f"My count: {len(neighbors)} Their count: {mycount} Friends: {payload['friend']} Recommended: {payload['recommendation']}", flush=True)
        neighbors.append(friend)
        return jsonify(payload)

    payload['friend'] = True
    payload['recommendation'] = rec
    print(f"My count: {len(neighbors)} Their count: {mycount} Friends: {payload['friend']} Recommended: {payload['recommendation']}", flush=True)
    neighbors.append(friend)

    return jsonify(payload)

@app.route('/map')
def map():
    return jsonify(neighbors)

@app.route('/info')
def info():
    return jsonify(neighbors) + jsonify(data)

@app.route('/store/<key>/<message>')
@app.route('/store/<key>/<message>/<steps>')
def store(key, message, steps = 0):
    steps = int(steps) + 1

    if random() < STORE_LIKELIHOOD * steps:
        data[key] = message
        return f'Stored in {steps} steps', 200
    else:
        neighbor_num = randint(1, len(neighbors)) - 1
        try:
            neighbor = neighbors[neighbor_num]
            print(f"{mynum} sending to {neighbor_num}", flush=True)
            return redirect(f'http://{neighbor}:5000/store/{key}/{message}/{steps}')
        except Exception as e:
            print(e, flush=True)
            return str(neighbors), 404

@app.route('/retrieve/<key>/<stayalive>')
@app.route('/retrieve/<key>/<stayalive>/<steps>')
def retrieve(key, stayalive, steps=0):
    steps = int(steps) + 1
    stayalive = int(stayalive)

    if steps > stayalive:
        payload = {
            key: 0,
            "steps": steps
        }
        code = 404
        return payload, code

    if key in data:
        payload = {
            key: data[key],
            "steps": steps
        }
        code = 200
        return payload, code
    else:
        asker = request.remote_addr
        if asker in neighbors and len(neighbors) == 1:
            payload = {
                key: 0,
                "steps": steps
            }
            code = 404
            return payload, code

        asker_key = neighbors.index(asker) if asker in neighbors else len(neighbors)
        neighbor_num = 0 if len(neighbors) == 2 else randint(2, len(neighbors)) - 2
        if neighbor_num >= asker_key:
            neighbor_num += 1
        try:
            neighbor = neighbors[neighbor_num]
            print(f"{mynum} retrieving from {neighbor}", flush=True)
            return redirect(f'http://{neighbor}:5000/retrieve/{key}/{stayalive}/{steps}')
        except Exception as e:
            print(e, flush=True)
            return str(neighbors), 404
