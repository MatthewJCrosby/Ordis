import os
from uuid import uuid4
from flask import Flask, g, request
import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_magql import MagqlExtension
from .gql import schema
from .db import get_session, Base
from flask_migrate import Migrate
from sqlalchemy import text
from flask_cors import CORS
from . import cli
from flask_jwt_extended import JWTManager



migrate = Migrate(compare_type=True)

def create_app(config_object="config.DevConfig"):
    app = Flask(__name__, instance_relative_config=True)
    jwt = JWTManager(app)
    app.config.from_object(config_object)
    app.config.from_pyfile("settings.py", silent=True)
    app.cli.add_command(cli.create_admin)
    CORS(app, origins=os.environ.get("CORS_ORIGINS", "http://localhost:5173").split(","), supports_credentials=True)

    limiter = Limiter(key_func=get_remote_address, default_limits=["500 per day", "50 per hour"])
    limiter.init_app(app)
 
    @app.before_request
    def request_id():
        #assign an id, log the request, open the session
        g.request_id = str(uuid4())
        app.logger.info(f"Request {g.request_id}: {request.method} {request.path}")
        g.db = get_session()
    

    @app.after_request
    def set_security_headers(response):
        response.headers["X-Request-ID"] = g.request_id

        #standard headers
        headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Referrer-Policy": "no-referrer",
            "X-Download-Options": "noopen",
            "X-Permitted-Cross-Domain-Policies": "none"
        }

        #CSP Policy
        if app.config.get('ENABLE_CSP', True):
            headers["Content-Security-Policy"] = (
               "default-src 'self'; "
               "script-src 'self'; "
               "style-src 'self'; "
               "img-src 'self' data:; "
               "connect-src 'self'" 
            )

        #production only headers
        if not app.debug and app.config.get('ENABLE_HSTS', True):
            headers["Strict-Transport-Security"] = ("max-age=31536000; includeSubDomains; preload")

        for header, value in headers.items():
            response.headers[header] = value

        return response

    root = logging.getLogger()
    if not root.handlers:
        handler = logging.StreamHandler()
        fmt = "[%(asctime)s] %(levelname)s in %(name)s: %(message)s"
        handler.setFormatter(logging.Formatter(fmt))
        root.addHandler(handler)
    root.setLevel(getattr(logging, app.config["LOG_LEVEL"], logging.INFO))


    @app.teardown_appcontext
    def _close_session(exc):
        session = getattr(g, "db", None)
        if session is not None:
            try:
                if exc is None:
                    session.commit()
                else:
                    session.rollback()
            finally:
                session.close()
    

    @app.get("/")
    @limiter.limit("10 per minute")
    def home():
        return {"status": "ok"}
    
    @app.get("/logger")
    def logger():
        app.logger.debug("Logger Message Example")
        return {"status": "ok"}
    
    @app.get("/pingdb")
    @limiter.limit("5 per minute")
    def ping_db():
        res = g.db.execute(text("select 1")).scalar_one()
        return {"db": res}
    
    from .health import bp as health_bp
    from.auth import auth_bp
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")

    MagqlExtension(schema).init_app(app)

    @app.errorhandler(404)
    def handle_404(e):
        return {"error": "Not Found"}, 404
    
    @app.errorhandler(500)
    def handle_500(e):
        return {"error": "Server Error"}, 500
    
    @app.errorhandler(429)
    def handle_rate_limit_exceeded(e):
        app.logger.warning(f"Rate limit exceeded for request {g.get('request_id', 'unknown')}")
        return {"error": "Rate limit exceeded", "request_id": g.request_id}, 429
    
    from . import models
    migrate.init_app(app, directory="migrations", metadata=Base.metadata)
    return app 

