from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
import os
from gql.bindables import bindables
from gql.schema import load_type_defs

from ariadne import graphql_sync, make_executable_schema, load_schema_from_path
from ariadne.explorer import ExplorerGraphiQL

from app.models import db, load_models
from .resolvers import query

migrate = Migrate()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    CORS(app)

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL is not set!")

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        load_models()

    type_defs = load_type_defs()
    schema = make_executable_schema(type_defs, *bindables)


    @app.route("/graphql", methods=["GET"])
    def graphql_playground():
        return ExplorerGraphiQL().html(None), 200

    @app.route("/graphql", methods=["POST"])
    def graphql_server():
        data = request.get_json()
        success, result = graphql_sync(schema, data, context_value=request, debug=app.debug)
        return jsonify(result)

    return app
