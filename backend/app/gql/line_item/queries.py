from flask import g
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from .. import schema
from app.models.line_item import LineItem
from app.gql.pagination import normalize_pagination

@schema.query.field("line_item", "LineItem", args={"id": "ID!"})
def resolve_line_item(parent, info, **kwargs):
    line_item_id = kwargs["id"]
    return g.db.execute(
    select(LineItem).where(LineItem.id == line_item_id)
).scalar_one_or_none()

@schema.query.field("line_items", "[LineItem!]", args={"limit": "Int", "offset": "Int"})
def resolve_line_items(parent, info, **kwargs):
    limit, offset = normalize_pagination(kwargs.get("limit"), kwargs.get("offset"))
    query = select(LineItem).order_by(LineItem.id).limit(limit).offset(offset)
    return g.db.execute(query).scalars().all()


