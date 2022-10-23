#!/usr/bin/python3
"""
RESTful API for class City
"""

from api.v1.views import app_views
from models import storage
from models.city import City
from flask import jsonify, abort, request


@app_views.route("/states/<state_id>/cities",
                 methods=['GET'], strict_slashes=False)
def get_city(state_id):
    """Reterive the City objects based on provided state Id"""
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404)
    city_objs = [obj.to_dict() for obj in state_obj.cities]
    return jsonify(city_objs), 200


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_city_id(city_id):
    """Reterive a City object based on provided city Id"""
    city_obj = storage.get('City', city_id)
    if city_obj is None:
        abort(404)
    return jsonify(city_obj.to_dict()), 200


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """Delete a city object"""
    city_obj = storage.get('City', city_id)
    if city_obj is None:
        abort(404)
    city_obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """Create a City object based on providede state_id"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif 'name' not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    else:
        state_obj = storage.get('State', state_id)
        if state_obj is None:
            abort(404)
        obj_data = request.get_json()
        obj_data['state_id'] = state_obj.id
        city_obj = City(**obj_data)
        city_obj.save()
        return jsonify(city_obj.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """Update a City object"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    city_obj = storage.get('City', city_id)
    if city_obj is None:
        abort(404)
    obj_data = request.get_json()
    city_obj.name = obj_data['name']
    return jsonify(city_obj.to_dict()), 200
