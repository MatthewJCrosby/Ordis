from flask import g
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from .. import schema
from app.models.order import Order
from app.gql.pagination import normalize_pagination

@schema.query.field("order", "Order", args={"id": "ID!"})
def resolve_order(parent, info, **kwargs):
    order_id = kwargs["id"]
    return g.db.execute(
        select(Order).where(Order.id == order_id)
    ).scalar_one_or_none()

@schema.query.field("orders", "[Order!]", args={"limit": "Int", "offset": "Int"})
def resolve_orders(parent, info, **kwargs):
    limit, offset = normalize_pagination(kwargs.get("limit"), kwargs.get("offset"))
    query = select(Order).order_by(Order.id).limit(limit).offset(offset)
    return g.db.execute(query).scalars().all()

