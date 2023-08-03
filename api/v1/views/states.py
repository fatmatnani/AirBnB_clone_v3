#!/usr/bin/python3
"""States api view module"""
from api.v1.views import app_views
from flask import (
    abort,
    jsonify,
    make_response,
    request
)
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """
        Retrieves a list of all the states
    """
    all_states = storage.all(State).values()
    state_list = [state.to_dict() for state in all_states]
    return jsonify(state_list), 200


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    """
    Retrieves a state by a given id
    """
    if state_id is None:
        abort(404)
    state = storage.get(State, state_id)  # get state object
    if state is None:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id=None):
    """
    Retrieves a state by a given id and deletes it
    """
    if state_id is None:
        abort(404)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.commit()

    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creates a State object based on the JSON body
    """
    kwargs = request.get_json()
    if not kwargs:
        return "Not a JSON", 400

    if 'name' not in kwargs:
        return 'Missing name', 400

    try:
        state = State(**kwargs)
        state.save()
    except TypeError:
        return "Not a JSON", 400

    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id=None):
    """
    Updates a State object based on the JSON body
    """
    kwargs = request.get_json()
    if not kwargs:
        return "Not a JSON", 400

    if 'name' not in kwargs:
        return 'Missing name', 400

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    for k in ("id", "created_at", "updated_at"):
        kwargs.pop(k, None)
    for k, v in kwargs.items():
        setattr(state, k, v)
    state.save()

    return jsonify(state.to_dict()), 200
