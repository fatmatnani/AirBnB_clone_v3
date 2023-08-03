#!/usr/bin/python3
<<<<<<< HEAD
"""State API routes"""

from flask import abort, jsonify, request
from api.v1.views import app_views
=======
"""
This module contains the State view methods.
"""
from flask import jsonify, request, abort, make_response
>>>>>>> 4e33e519879b9ae6fb05714705014b8094006367
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Gets all State objects"""
    all_states = storage.all(State).values()
    list_states = [state.to_dict() for state in all_states]
    return jsonify(list_states)


@app_views.route('/states/<state_id>',
                 methods=['GET', 'DELETE', 'PUT', 'POST'],
                 strict_slashes=False)
def get_state(state_id):
    """Gets a State object by id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
<<<<<<< HEAD
    """Creates a new State object"""
    req = request.get_json()
    if not req:
        abort(400, 'Not a JSON')
    if 'name' not in req:
        abort(400, 'Missing name')

    new_state = State(**req)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
=======
    """Create a State object."""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    else:
        data = request.get_json()
        instance = State(**data)
        instance.save()
        return jsonify(instance.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
>>>>>>> 4e33e519879b9ae6fb05714705014b8094006367
def update_state(state_id):
    """Updates a State object by id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    req = request.get_json()
    if not req:
        abort(400, 'Not a JSON')

    for k, v in req.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object by id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    return jsonify({}), 200
