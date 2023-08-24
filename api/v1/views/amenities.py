#!/usr/bin/python3
"""Create a new route"""
from flask import jsonify, abort, request
from . import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def amenities_get():
    """return json file with the dictionary of all amenities"""
    list_amenities = []
    for amenities in storage.all(Amenity).values():
        list_amenities.append(amenities.to_dict())
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenities_get_with_id(amenity_id):
    """returns a json file with the dictionary of an object by its id"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def amenities_post():
    """returns a json file with the dictionary of a newly added object"""
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    new_amenity = Amenity(name=data['name'])
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def amenities_delete(amenity_id):
    """returns a json file with an empty dictionary if successfully deleted"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def amenities_put(amenity_id):
    """returns a json file with the dictionary of an
    object that has been updated"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    ignore = ['id', 'created_at', 'updated_at']
    for k, v in data.items():
        if k not in ignore:
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict()), 200
