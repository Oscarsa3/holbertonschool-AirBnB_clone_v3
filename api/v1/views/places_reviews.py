#!/usr/bin/python3
"""Create a new route"""
from flask import jsonify, abort, request
from . import app_views
from models import storage
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews_get(place_id):
    """return json file with the dictionary of all places"""
    obj_place = storage.get(Place, place_id)
    if obj_place is None:
        abort(404)
    list_reviews = []
    for review in storage.all(Review).values():
        if review.place_id == place_id:
            list_reviews.append(review.to_dict())
    return jsonify(list_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def reviews_get_with_id(review_id):
    """returns a json file with the dictionary of an object by its id"""
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def reviews_post(place_id):
    """returns a json file with the dictionary of a newly added object"""
    obj_place = storage.get(Place, place_id)
    if obj_place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400
    elif storage.get(User, data['user_id']) is None:
        abort(404)
    elif 'text' not in data:
        return jsonify({"error": "Missing text"}), 400
    new_review = Review(**data, place_id=place_id)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def reviews_delete(review_id):
    """returns a json file with an empty dictionary if successfully deleted"""
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def reviews_put(review_id):
    """returns a json file with the dictionary of an
    object that has been updated"""
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    ignore = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']
    for k, v in data.items():
        if k not in ignore:
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict()), 200
