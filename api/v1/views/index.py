#!/usr/bin/python3
"""Create a new route"""
from flask import jsonify
from . import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """return json file with the status of our api"""
    dicc = {"status": "OK"}
    return jsonify(dicc)
