from sqlalchemy.exc import IntegrityError
from flask import g


def commit_or_rollback(entity_type, operation):
    try:
        g.db.flush()
        g.db.commit()
    except IntegrityError:
        g.db.rollback()
        raise ValueError(f"Failed to {operation} {entity_type}")