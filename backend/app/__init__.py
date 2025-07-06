import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from ariadne import graphql_sync, make_executable_schema, load_schema_from_path
from ariadne.explorer import ExplorerGraphiQL

from .resolvers import query  # assumes resolvers.py has a QueryType() instance

# Initialize SQLAlchemy and Migrate
db = SQLAlchemy()
migrate = Migrate()

# Load GraphQL schema and bind resolvers
type_defs = load_schema_from_path(os.path.join(os.path.dirname(__file__), "schema.graphql"))
schema = make_executable_schema(type_defs, query)

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configure database
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL is not set!")
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    # Optional: Import models to register them with SQLAlchemy
    from . import models

    # GraphQL GET (GraphiQL UI)
    @app.route("/graphql", methods=["GET"])
    def graphql_playground():
        return ExplorerGraphiQL().html(None), 200

    # GraphQL POST (queries and mutations)
    @app.route("/graphql", methods=["POST"])
    def graphql_server():
        data = request.get_json()
        success, result = graphql_sync(schema, data, context_value=request, debug=app.debug)
        return jsonify(result)

    return app
