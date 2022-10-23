#!/usr/bin/python3
"""
RESTful API for class State
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def states():
    """Reterive state objects"""
    new_dict = [obj.to_dict() for obj in storage.all('State').values()]
    return jsonify(new_dict)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states_id(state_id):
    """Reterive state objects with specified state_id"""
    new_dict = storage.get('State', state_id)
    if new_dict is None:
        abort(404)
    else:
        return jsonify(new_dict.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete state objects with specified state_id"""
    obj = storage.get('State', state_id)
    if obj is None:
        abort(404)
    else:
        obj.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a new state objects"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    else:
        obj_data = request.get_json()
        obj = State(**obj_data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update a state objects"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    obj = storage.get('State', state_id)
    if obj is None:
        abort(404)
    obj_data = request.get_json()
    obj.name = obj_data['name']
    obj.save()
    return jsonify(obj.to_dict()), 200
