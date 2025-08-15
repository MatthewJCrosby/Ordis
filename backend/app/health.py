from flask import Blueprint

bp = Blueprint("health", __name__)

@bp.get("/healthz")
def healthz():
    return {"status": "ok"}

