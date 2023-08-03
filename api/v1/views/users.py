#!/usr/bin/python3
"""
This file contains the User module
"""
from flask import Flask, request, jsonify, make_response
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<string:user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object by its ID"""
    user = storage.get(User, user_id)
    if not user:
        return make_response(jsonify({"error": "Not found"}), 404)
    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object by its ID"""
    user = storage.get(User, user_id)
    if not user:
        return make_response(jsonify({"error": "Not found"}), 404)

    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User object"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    data = request.get_json()
    if 'email' not in data:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if 'password' not in data:
        return make_response(jsonify({"error": "Missing password"}), 400)

    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<string:user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object by its ID"""
    user = storage.get(User, user_id)
    if not user:
        return make_response(jsonify({"error": "Not found"}), 404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    data = request.get_json()
    data.pop('id', None)
    data.pop('email', None)
    data.pop('created_at', None)
    data.pop('updated_at', None)

    for key, value in data.items():
        setattr(user, key, value)

    user.save()
    return jsonify(user.to_dict()), 200
