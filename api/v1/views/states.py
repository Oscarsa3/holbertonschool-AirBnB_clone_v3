#!/usr/bin/python3
"""Create a new route"""
from flask import jsonify, abort, request
from . import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states_get():
    """return json file with the dictionary of all states"""
    objs = []
    for obj in storage.all(State).values():
        objs.append(obj.to_dict())
    return jsonify(objs)


@app_views.route('/states/<s_id>', methods=['GET'], strict_slashes=False)
def states_get_with_id(s_id):
    """returns a json file with the dictionary of an object by its id"""
    obj = storage.get(State, s_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def states_post():
    """returns a json file with the dictionary of a newly added object"""
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    new_state = State(name=data['name'])
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<s_id>', methods=['DELETE'], strict_slashes=False)
def states_delete(s_id):
    """returns a json file with an empty dictionary if successfully deleted"""
    obj = storage.get(State, s_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<s_id>', methods=['PUT'], strict_slashes=False)
def states_put(s_id):
    """returns a json file with the dictionary of an
    object that has been updated"""
    obj = storage.get(State, s_id)
    if obj is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({"error": "not a json"}), 400
    ignore = ['id', 'created_at', 'updated_at']
    for k, v in data.items():
        if k not in ignore:
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict()), 200
