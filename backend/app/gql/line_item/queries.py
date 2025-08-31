from flask import g
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.gql.utils import get_entities, get_entity
from .. import schema
from app.models.line_item import LineItem
from app.gql.pagination import normalize_pagination

@schema.query.field("line_item", "LineItem", args={"id": "ID!"})
def resolve_line_item(parent, info, **kwargs):
    line_item_id = kwargs["id"]
    return get_entity(LineItem, line_item_id)

@schema.query.field("line_items", "[LineItem!]", args={"limit": "Int", "offset": "Int"})
def resolve_line_items(parent, info, **kwargs):
    return get_entities(LineItem, **kwargs)


