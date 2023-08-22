#!/usr/bin/python3
"""starts a Flask web application"""
from flask import Flask, render_template, make_response, jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exception=None):
    """close method"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """return a json with 404 error"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
