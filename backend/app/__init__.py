import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv

from ariadne import graphql_sync, make_executable_schema, load_schema_from_path
from ariadne.explorer import ExplorerGraphiQL

from app.models import db  
from app.models import load_models  # helper that dynamically imports all model files
from .resolvers import query

# Initialize SQLAlchemy and Migrate
db = SQLAlchemy()
migrate = Migrate()

# Load GraphQL schema and bind resolvers
type_defs = load_schema_from_path(os.path.join(os.path.dirname(__file__), "schema.graphql"))
schema = make_executable_schema(type_defs, query)

def create_app():
    load_dotenv()
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

    # Dynamically import all models from models folder
    with app.app_context():
        load_models()

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
