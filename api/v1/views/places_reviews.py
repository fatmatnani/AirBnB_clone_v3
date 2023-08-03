#!/usr/bin/python3
"""
This file contains the Review module
"""
from flask import Flask, request, jsonify, make_response, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<string:place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews_by_place(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<string:review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object by its ID"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<string:review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object by its ID"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<string:place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Creates a Review object associated with a specific Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    data = request.get_json()
    if 'user_id' not in data:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if 'text' not in data:
        return make_response(jsonify({"error": "Missing text"}), 400)

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<string:review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object by its ID"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    data = request.get_json()
    data.pop('id', None)
    data.pop('user_id', None)
    data.pop('place_id', None)
    data.pop('created_at', None)
    data.pop('updated_at', None)

    for key, value in data.items():
        setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict()), 200
