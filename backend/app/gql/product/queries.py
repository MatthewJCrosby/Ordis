from flask import g
from sqlalchemy import select

from app.gql.utils import get_entity, get_entities
from .. import schema
from app.models.product import Product
from app.gql.pagination import normalize_pagination

@schema.query.field("product", "Product", args={"id": "ID!"})
def resolve_product(parent, info, **kwargs):
    product_id = kwargs["id"]
    return get_entity(Product, product_id)


@schema.query.field("products", "[Product!]", args={"limit": "Int", "offset": "Int"})
def resolve_products(parent, info, **kwargs):
    return get_entities(Product, **kwargs)


