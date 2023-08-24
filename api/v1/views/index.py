#!/usr/bin/python3
"""Create a new route"""
from flask import jsonify
from . import app_views
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.user import User


@app_views.route('/status', methods=['GET'])
def status():
    """return json file with the status of our api"""
    dictionary = {"status": "OK"}
    return jsonify(dictionary)


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
