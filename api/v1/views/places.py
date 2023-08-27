#!/usr/bin/python3
"""Create a new route"""
from flask import jsonify, abort, request
from . import app_views
from models import storage
from models.user import User
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places_get(city_id):
    """return json file with the dictionary of all places"""
    obj_city = storage.get(City, city_id)
    if obj_city is None:
        abort(404)
    list_places = []
    for place in storage.all(Place).values():
        if place.city_id == city_id:
            list_places.append(place.to_dict())
    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def places_get_with_id(place_id):
    """returns a json file with the dictionary of an object by its id"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def places_post(city_id):
    """returns a json file with the dictionary of a newly added object"""
    obj_state = storage.get(City, city_id)
    if obj_state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400
    elif storage.get(User, data['user_id']) is None:
        abort(404)
    elif 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    new_place = Place(**data, city_id=city_id)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def places_search():
    """Search for places"""
    # {"states": [ids], "cities": [ids], "amenities": [ids]}
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif len(data) == 0 or all(len(v) == 0 for v in data.values()):
        return [obj.to_dict() for obj in storage.all(Place).values()]

    show = None
    if data.get("cities") and len(data.get("cities")) > 0:
        cities = data["cities"]
        show = [v for v in storage.all(Place).values() if v.id in cities]
    if len(data["states"]) > 0:
        states = data["states"]
        if show:
            cities = [v.id for v in storage.all(
                City).values() if v.id in states]
            show = [place
                    for place in storage.all(Place).values()
                    if place.id in cities and place.id
                    not in [v.id for v in show]] + show
        else:
            show = [v for v in storage.all(Place).values()]
    flag = 0  # flag to check if amenities exist
    new_list_places = []
    if data.get("amenities") and len(data.get("amenities")) > 0:
        flag = 1
        exist = []
        for value in show:
            for amen in value.amenties:
                if amen.id in data["amenities"]:
                    exist.append(True)
                else:
                    exist.append(False)
            if all(exist):
                new_list_places.append(value.to_dict())
    if flag:
        return jsonify(new_list_places)
    else:
        return jsonify([v.to_dict() for v in show])


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def places_delete(place_id):
    """returns a json file with an empty dictionary if successfully deleted"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def places_put(place_id):
    """returns a json file with the dictionary of an
    object that has been updated"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    ignore = ['id', 'created_at', 'updated_at', 'user_id', 'city_id']
    for k, v in data.items():
        if k not in ignore:
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict()), 200
