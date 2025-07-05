# app/routes.py

from flask import Blueprint, jsonify
from .models import Customer

bp = Blueprint("main", __name__)

@bp.route("/")
def ping():
    return jsonify({"message": "Hello, Welcome to the home page"})


@bp.route("/customers")
def get_customers():
    customers = Customer.query.all()
    return jsonify([{
        "id": c.id,
        "first_name": c.first_name,
        "last+name": c.last_name,
        "email": c.email,
        "phone": c.phone
    } for c in customers])
