from flask import g
from sqlalchemy import select

from app.gql.pagination import normalize_pagination

# Helper to reduce boilerplate code for fetching entities
def get_entity(entity_class, id, error=None):
    entity = g.db.execute(select(entity_class).where(entity_class.id == id)).scalar_one_or_none()
    if not entity:
        if error:
            raise ValueError(error)
        else:
            raise ValueError(f"{entity_class.__name__} with id: {id} not found")
    return entity

def get_entities(entity_class, **kwargs):
    limit, offset = normalize_pagination(kwargs.get("limit"), kwargs.get("offset"))
    query = select(entity_class).order_by(entity_class.id).limit(limit).offset(offset)
    return g.db.execute(query).scalars().all()

# Helper to reduce boilerplate code for updating entities and dynamically set non-null passed in data with a security mechanism to specify allowed fields
def update_entity(entity, input_data, allowed_fields=None):
    for key, value in input_data.items():
        if value is not None and (not allowed_fields or key in allowed_fields):
            setattr(entity, key, value)
        
def delete_entity(entity_class, id, error=None):
    entity = get_entity(entity_class, id, error=error)
    g.db.delete(entity)
    return True