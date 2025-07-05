from flask import Blueprint
from flask_graphql import GraphQLView
from .schema import schema

bp = Blueprint("main", __name__)

@bp.route('/')
def index():
    return "Hello from Flask!"

def init_routes(app):
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
    )