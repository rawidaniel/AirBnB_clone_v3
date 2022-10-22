#!/usr/bin/python3
'''
    flask with general routes
    routes:
        /status:    display "status":"OK"
'''
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """return status ok json formatted"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def count():
    """Return count of each classes"""
    count_class = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
        }
    return jsonify(count_class)
