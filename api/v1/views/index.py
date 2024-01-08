#!/usr/bin/python3
"""
Status and stats endpoints
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """
    The "status" route.
    Returns "status": "OK" json
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """
    Returns the count of each object
    """
    results = {}
    names = {"Amenity": "amenities",
             "City": "cities",
             "Place": "places",
             "Review": "reviews",
             "State": "states",
             "User": "users"}

    for k, v in sorted(names.items()):
        results[v] = storage.count(k)

    return jsonify(results)
