from flask import g
from sqlalchemy import select
from .. import schema
from app.models.product import Product
from app.gql.pagination import normalize_pagination

@schema.query.field("product", "Product", args={"id": "ID!"})
def resolve_product(parent, info, **kwargs):
    product_id = kwargs["id"]
    return g.db.execute(
        select(Product).where(Product.id == product_id)
    ).scalar_one_or_none()


@schema.query.field("products", "[Product!]", args={"limit": "Int", "offset": "Int"})
def resolve_products(parent, info, **kwargs):
    limit, offset = normalize_pagination(kwargs.get("limit"), kwargs.get("offset"))
    query = select(Product).order_by(Product.id).limit(limit).offset(offset)
    return g.db.execute(query).scalars().all()


