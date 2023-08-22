#!/usr/bin/python3
"""Create a new route"""
from flask import jsonify
from . import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """return json file with the status of our api"""
    dicc = {"status": "OK"}
    return jsonify(dicc)


@app_views.route('/stats', methods=['GET'])
def stats():
    """return the number of each objects by type"""
    dicc = {"amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)}
    return jsonify(dicc)
