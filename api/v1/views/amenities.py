#!/usr/bin/python3
"""
RESTful API for class Amenity
"""

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def get_amenity():
    """Reterive all Amenity objects"""
    amenity_objs = [obj.to_dict() for obj in storage.all("Amenity").values()]
    return jsonify(amenity_objs), 200


@app_views.route("/amenities/<amenity_id>",
                 methods=['GET'], strict_slashes=False)
def get_amenity_id(amenity_id):
    """Reterive a Amenity objects based on provided Id"""
    amenity_obj = storage.get('Amenity', amenity_id)
    if amenity_obj is None:
        abort(404)
    return jsonify(amenity_obj.to_dict()), 200


@app_views.route("/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete a amenity object given amenity_id"""
    amenity_obj = storage.get('Amenity', amenity_id)
    if amenity_obj is None:
        abort(404)
    amenity_obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Create a amenity object"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif 'name' not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    else:
        obj_data = request.get_json()
        amenity_obj = Amenity(**obj_data)
        amenity_obj.save()
        return jsonify(amenity_obj.to_dict()), 201


@app_views.route("/amenities/<amenity_id>",
                 methods=["PUT"], strict_slashes=False)
def update_amenity(amenity_id):
    """Update existing amenity object"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    amenity_obj = storage.get('Amenity', amenity_id)
    if amenity_obj is None:
        abort(404)
    obj_data = request.get_json()
    amenity_obj.name = obj_data['name']
    amenity_obj.save()
    return jsonify(amenity_obj.to_dict()), 200
