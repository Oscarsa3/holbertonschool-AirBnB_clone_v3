#!/usr/bin/python3
"""Create a new route"""
from flask import jsonify, abort, request
from . import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def amenity_get(place_id):
    """return json file with the dictionary of all places"""
    obj_place = storage.get(Place, place_id)
    if obj_place is None:
        abort(404)
    list_amenities = []
    for amenity in storage.all(Amenity).values():
        if amenity.place_id == place_id:
            list_amenities.append(amenity.to_dict())
    return jsonify(list_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def amenity_post(place_id):
    """returns a json file with the dictionary of a newly added object"""
    obj_place = storage.get(Place, place_id)
    obj_amenity = storage.get(Amenity, amenity_id)
    if obj_place is None or obj_amenity is None:
        abort(404)
    exist = 0
    for amenity in storage.all(Amenity).values():
        if amenity.place_id == place_id:
            return jsonify(amenity.to_dict()), 200
    new_amenity = Amenity()
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def amenity_delete(place_id, amenity_id):
    """returns a json file with an empty dictionary if successfully deleted"""
    obj_place = storage.get(Place, place_id)
    obj_amenity = storage.get(Amenity, amenity_id)
    if obj_place is None or obj_amenity is None:
        abort(404)
    exist = 0
    for amenity in storage.all(Amenity).values():
        if amenity.place_id == place_id:
            exist = 1
    if exist == 0:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200
