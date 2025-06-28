# app/routes.py

from flask import Blueprint, jsonify

bp = Blueprint("main", __name__)

@bp.route("/")
def ping():
    return jsonify({"message": "Hello, Welcome to the home page"})
