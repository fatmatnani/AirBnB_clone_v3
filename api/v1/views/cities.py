#!/usr/bin/python3
"""
This file contains the City module
"""

from flask import Flask, request, jsonify, make_response
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<string:state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if not state:
        return make_response(jsonify({"error": "Not found"}), 404)

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object by its ID"""
    city = storage.get(City, city_id)
    if not city:
        return make_response(jsonify({"error": "Not found"}), 404)

    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object by its ID"""
    city = storage.get(City, city_id)
    if not city:
        return make_response(jsonify({"error": "Not found"}), 404)

    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Creates a City object associated with a specific State"""
    state = storage.get(State, state_id)
    if not state:
        return make_response(jsonify({"error": "Not found"}), 404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    data = request.get_json()
    if 'name' not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)

    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a City object by its ID"""
    city = storage.get(City, city_id)
    if not city:
        return make_response(jsonify({"error": "Not found"}), 404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    data = request.get_json()
    data.pop('id', None)
    data.pop('state_id', None)
    data.pop('created_at', None)
    data.pop('updated_at', None)

    for key, value in data.items():
        setattr(city, key, value)

    city.save()
    return jsonify(city.to_dict()), 200
