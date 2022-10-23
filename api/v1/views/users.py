#!/usr/bin/python3
"""
RESTful API for class User
"""

from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, abort, request


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def get_users():
    """Reterive all user objects"""
    user_objs = [obj.to_dict() for obj in storage.all('User').values()]
    return jsonify(user_objs), 200


@app_views.route("/users/<user_id>",
                 methods=['GET'], strict_slashes=False)
def get_user_id(user_id):
    """Reterive a user objects based on provided Id"""
    user_obj = storage.get('User', user_id)
    if user_obj is None:
        abort(404)
    return jsonify(user_obj.to_dict()), 200


@app_views.route("/users/<user_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """Delete a user object given user_id"""
    user_obj = storage.get('User', user_id)
    if user_obj is None:
        abort(404)
    user_obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Create new user object"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif 'email' not in request.get_json():
        return jsonify({"error": "Missing email"}), 400
    elif 'password' not in request.get_json():
        return jsonify({"error": "Missing password"}), 400
    else:
        obj_data = request.get_json()
        user_obj = User(**obj_data)
        user_obj.save()
        return jsonify(user_obj.to_dict()), 201


@app_views.route("/users/<user_id>",
                 methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """Update existing user object"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    user_obj = storage.get('User', user_id)
    if user_obj is None:
        abort(404)
    obj_data = request.get_json()
    ignore = ('id', 'email', 'created_at', 'updated_at')
    for k in obj_data.keys():
        if k in ignore:
            pass
        else:
            setattr(user_obj, k, obj_data[k])
    user_obj.save()
    return jsonify(user_obj.to_dict()), 200
