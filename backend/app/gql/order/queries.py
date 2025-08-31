from flask import g
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.gql.utils import get_entity, get_entities
from .. import schema
from app.models.order import Order
from app.gql.pagination import normalize_pagination

@schema.query.field("order", "Order", args={"id": "ID!"})
def resolve_order(parent, info, **kwargs):
    order_id = kwargs["id"]
    return get_entity(Order, order_id)

@schema.query.field("orders", "[Order!]", args={"limit": "Int", "offset": "Int"})
def resolve_orders(parent, info, **kwargs):
    return get_entities(Order, **kwargs)

