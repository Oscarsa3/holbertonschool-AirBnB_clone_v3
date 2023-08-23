#!/usr/bin/python3
"""Create a new route"""
from flask import jsonify, abort, request
from . import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<s_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_get(s_id):
    """return json file with the dictionary of all states"""
    obj_state = storage.get(State, s_id)
    if obj_state is None:
        abort(404)
    list_cities = []
    for city in storage.all(City).values():
        if city.state_id == s_id:
            list_cities.append(city.to_dict())
    return jsonify(list_cities)


@app_views.route('/cities/<c_id>', methods=['GET'],
                 strict_slashes=False)
def cities_get_with_id(c_id):
    """returns a json file with the dictionary of an object by its id"""
    obj = storage.get(City, c_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/states/<s_id>/cities', methods=['POST'],
                 strict_slashes=False)
def cities_post(s_id):
    """returns a json file with the dictionary of a newly added object"""
    obj_state = storage.get(State, s_id)
    if obj_state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    new_city = City(name=data['name'], state_id=s_id)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<c_id>', methods=['DELETE'],
                 strict_slashes=False)
def cities_delete(c_id):
    """returns a json file with an empty dictionary if successfully deleted"""
    obj = storage.get(City, c_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<c_id>', methods=['PUT'],
                 strict_slashes=False)
def cities_put(c_id):
    """returns a json file with the dictionary of an
    object that has been updated"""
    obj = storage.get(City, c_id)
    if obj is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({"error": "not a json"}), 400
    ignore = ['id', 'created_at', 'updated_at', 'state_id']
    for k, v in data.items():
        if k not in ignore:
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict()), 200
