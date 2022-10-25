#!/usr/bin/python3
"""
RESTful API for class City
"""

from api.v1.views import app_views
from models import storage
from models.place import Place
from flask import jsonify, abort, request


@app_views.route("/cities/<city_id>/places",
                 methods=['GET'], strict_slashes=False)
def get_place(city_id):
    """Reterive the place objects based on provided city Id"""
    city_obj = storage.get('City', city_id)
    if city_obj is None:
        abort(404)
    place_objs = [obj.to_dict() for obj in city_obj.places]
    return jsonify(place_objs), 200


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def get_place_id(place_id):
    """Reterive a place object based on provided place Id"""
    place_obj = storage.get('Place', place_id)
    if place_obj is None:
        abort(404)
    return jsonify(place_obj.to_dict()), 200


@app_views.route("/places/<place_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_Place(place_id):
    """Delete a place object"""
    place_obj = storage.get('Place', place_id)
    if place_obj is None:
        abort(404)
    place_obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """Create new place object based on providede city_id"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif 'user_id' not in request.get_json():
        return jsonify({"error": "Missing user_id"}), 400
    elif 'name' not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    else:
        obj_data = request.get_json()
        city_obj = storage.get('City', city_id)
        user_obj = storage.get('User', obj_data['user_id'])
        if city_obj is None or user_obj is None:
            abort(404)
        obj_data['city_id'] = city_obj.id
        obj_data['user_id'] = user_obj.id
        place_obj = Place(**obj_data)
        place_obj.save()
        return jsonify(place_obj.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Update existing place  object"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    place_obj = storage.get('Place', place_id)
    if place_obj is None:
        abort(404)
    obj_data = request.get_json()
    ignore = ('id', 'user_id', 'city_id', 'created_at', 'updated_at')
    for k, v in obj_data.items():
        if k not in ignore:
            setattr(place_obj, k, v)
    place_obj.save()
    return jsonify(place_obj.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def post_places_search():
    """
    retrieves all Place objects depending of the JSON in the body
    of the request.
    """
    if request.get_json() is not None:
        data = request.get_json()
        states = data.get('states', [])
        cities = data.get('cities', [])
        amenities = data.get('amenities', [])
        amenity_objs = []
        for amenity_id in amenities:
            amenity = storage.get('Amenity', amenity_id)
            amenity_objs.append(amenity)
        if states == cities == []:
            places = storage.all('Place').values()
        else:
            places = []
            for state_id in states:
                state = storage.get('State', state_id)
                state_cities = state.cities
                for city in state_cities:
                    if city.id not in cities:
                        cities.append(city.id)
            for city_id in cities:
                city = storage.get('City', city_id)
                for place in city.places:
                    places.append(place)
        place_confirmed = []
        for place in places:
            place_amenity = place.amenities
            place_confirmed.append(place.to_dict())
            for amenity in amenity_objs:
                if amenity not in place_amenity:
                    place_confirmed.pop()
                    break
        return jsonify(place_confirmed)
    else:
        return jsonify({"error": "Not a JSON"}), 400
