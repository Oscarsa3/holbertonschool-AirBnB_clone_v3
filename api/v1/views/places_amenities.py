#!/usr/bin/python3
"""Create a new route"""
from flask import jsonify, abort, request
from . import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
import os


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def amenity_get(place_id):
    """return json file with the dictionary of all places"""
    obj_place = storage.get(Place, place_id)
    if obj_place is None:
        abort(404)
    list_amenities = []
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        list_amenity = obj_place.amenities
        for amenity in list_amenity:
            list_amenities.append(amenity.to_dict)
    else:
        for amenity in obj_place.amenity_ids:
            list_amenities.append(storage.get(Amenity, amenity).to_dict)
    return jsonify(list_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def amenity_post(place_id):
    """returns a json file with the dictionary of a newly added object"""
    obj_place = storage.get(Place, place_id)
    obj_amenity = storage.get(Amenity, amenity_id)
    if obj_place is None:
        abort(404)
    if obj_amenity is None:
        abort(404)
    exist = 0
    for amenity in storage.all(Amenity).values():
        if place.amenity.place_id == place_id and \
         place.amenity_amenity_id == amenity_id:
            return jsonify(amenity.to_dict()), 200
    setattr(obj_place, amenity.amenity_id, amenity_id)
    storage.save()
    return jsonify(obj_amenity.to_dict()), 201


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def amenity_delete(place_id, amenity_id):
    """returns a json file with an empty dictionary if successfully deleted"""
    obj_place = storage.get(Place, place_id)
    obj_amenity = storage.get(Amenity, amenity_id)
    if obj_place is None:
        abort(404)
    if obj_amenity is None:
        abort(404)
    exist = 0
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        if obj_amenity in obj_place.amenities:
            exist = 1
    else:
        if amenity_id in obj_place.amenity_ids:
            exist = 1
    if exist == 0:
        abort(404)
    storage.delete(obj_amenity)
    storage.save()
    return jsonify({}), 200
