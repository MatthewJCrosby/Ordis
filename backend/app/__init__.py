from flask import Flask

def create_app(config_object="config.DevConfig"):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)
    app.config.from_pyfile("settings.py", silent=True)
    @app.get("/")
    def home():
        return {"status": "ok"}
    return app

