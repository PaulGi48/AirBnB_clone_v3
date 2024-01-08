#!/usr/bin/python3
"""
Review endpoints
"""
from api.v1.views import app_views
from models import storage, Review
from flask import abort, request, jsonify


@app_views.route(
    '/places/<place_id>/reviews',
    strict_slashes=False,
    methods=['GET'])
def review_list(place_id):
    """
    Retrieves the list of all Review objects of a Place
    """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    review_list = [review.to_dict() for review in place.reviews]
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def review_by_id(review_id):
    """
    Retrieves review by review id. If review_id not linked to review,
    raise 404.
    """
    reviews = storage.all("Review").values()
    review = next(filter(lambda x: x.id == review_id, reviews), None)
    return jsonify(review.to_dict()) if review else abort(404)


@app_views.route(
    '/reviews/<review_id>',
    strict_slashes=False,
    methods=['DELETE'])
def delete_review(review_id):
    """
    Deletes review by id. If review_id not linked to review, raise 404
    Returns empty dict with status 200
    """
    reviews = storage.all("Review").values()
    review = next(filter(lambda x: x.id == review_id, reviews), None)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route(
    '/places/<place_id>/reviews',
    strict_slashes=False,
    methods=['POST'])
def create_review(place_id):
    """
    Creates new review. If request body not valid JSON, raises 400
    If dict does not contain 'name' key, raise 400
    Returns review object with status 201
    """
    if not request.get_json():
        abort(400, "Not a JSON")

    kwargs = request.get_json()

    a = storage.get("Place", place_id)
    if a is None:
        abort(404)

    if not kwargs.get('user_id'):
        abort(400, "Missing user_id")
    if not kwargs.get('text'):
        abort(400, 'Missing text')

    a = storage.get("User", kwargs["user_id"])
    if a is None:
        abort(404)

    my_review = Review(place_id=place_id, **kwargs)
    storage.new(my_review)
    storage.save()

    return jsonify(my_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    """
    Updates review. If request not valid JSON, raises 400.
    If review_id not linked to review object, raise 404
    Returns review object with status code 200
    """
    reviews = storage.all("Review").values()
    review = next(filter(lambda x: x.id == review_id, reviews), None)
    if not review:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    args = request.get_json()

    review.text = args.get('text', review.text)

    for k, v in args.items():
        if k not in ['id', 'created_at', 'updated_at', 'user_id', 'place_id']:
            setattr(review, k, v)

    storage.save()

    return jsonify(review.to_dict()), 200

    # might need to ignore keys explireviewly
