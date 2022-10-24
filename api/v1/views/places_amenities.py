#!/usr/bin/python3
'''
    RESTful API for class Amenity
'''
from flask import jsonify, abort
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity
from models.place import Place
from os import getenv


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get__amenity_by_place(place_id):
    '''
        return amenity by place, json form
    '''
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == 'db':
        amenity_objs = place.amenities
    else:
        amenity_objs = place.amenity_ids
    amenity_list = [r.to_dict() for r in amenity_objs]
    return jsonify(amenity_list), 200


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    '''
        delete amenity obj to a place given review_id and amenity_id
    '''
    place = storage.get('Place', place_id)
    amenity = storage.get('Amenity', amenity_id)
    if place is None or amenity is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        amenity_objs = place.amenities
    else:
        amenity_objs = place.amenity_ids
    if amenity not in amenity_objs:
        abort(404)
    amenity_objs.remove(amenity)
    place.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def create_place_amenity(place_id, amenity_id):
    '''
        create new amenity obj through place association using POST
    '''
    place = storage.get("Place", place_id)
    amenity = storage.get('Amenity', amenity_id)
    if place is None or amenity is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        amenity_objs = place.amenities
    else:
        amenity_objs = place.amenity_ids
    if amenity in amenity_objs:
        return jsonify(amenity.to_dict()), 200
    amenity_objs.append(amenity)
    place.save()
    return jsonify(amenity.to_dict()), 201
