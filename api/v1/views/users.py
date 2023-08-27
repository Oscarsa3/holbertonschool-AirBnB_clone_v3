#!/usr/bin/python3
"""Create a new route"""
from flask import jsonify, abort, request
from . import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users_get():
    """return json file with the dictionary of all users"""
    objs = []
    for obj in storage.all(User).values():
        objs.append(obj.to_dict())
    return jsonify(objs)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def users_get_with_id(user_id):
    """returns a json file with the dictionary of an object by its id"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def users_post():
    """returns a json file with the dictionary of a newly added object"""
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif 'email' not in data:
        return jsonify({"error": "Missing email"}), 400
    elif 'password' not in data:
        return jsonify({"error": "Missing password"}), 400
    new_user = User(email=data['email'], password=data['password'])
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def users_delete(user_id):
    """returns a json file with an empty dictionary if successfully deleted"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def users_put(user_id):
    """returns a json file with the dictionary of an
    object that has been updated"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    ignore = ['id', 'created_at', 'updated_at', 'email']
    for k, v in data.items():
        if k not in ignore:
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict()), 200
