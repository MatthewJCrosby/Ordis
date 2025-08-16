from flask import Flask
import logging
from flask_magql import MagqlExtension
from .gql import schema

def create_app(config_object="config.DevConfig"):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)
    app.config.from_pyfile("settings.py", silent=True)


    root = logging.getLogger()
    if not root.handlers:
        handler = logging.StreamHandler()
        fmt = "[%(asctime)s] %(levelname)s in %(name)s: %(message)s"
        handler.setFormatter(logging.Formatter(fmt))
        root.addHandler(handler)
    root.setLevel(getattr(logging, app.config["LOG_LEVEL"], logging.INFO))

    @app.get("/")
    def home():
        return {"status": "ok"}
    
    @app.get("/logger")
    def logger():
        app.logger.debug("Logger Message Example")
        return {"status": "ok"}
    
    from .health import bp as health_bp
    app.register_blueprint(health_bp)

    MagqlExtension(schema).init_app(app)

    @app.errorhandler(404)
    def handle_404(e):
        return {"error": "Not Found"}, 404
    
    @app.errorhandler(500)
    def handle_404(e):
        return {"error": "Server Error"}, 500
    
    
    return app

