from flask import g
from sqlalchemy import select
from .. import schema
from app.models.customer import Customer
from app.gql.pagination import normalize_pagination

@schema.query.field("customer", "Customer", args={"id": "ID!"})
def resolve_customer(_, info, **kwargs):
    cid = kwargs["id"]
    return g.db.execute(
        select(Customer).where(Customer.id == cid)
    ).scalar_one_or_none()

@schema.query.field("customers", "[Customer!]", args={"limit": "Int", "offset": "Int"})
def resolve_customers(_, info, limit=None, offset=None):
    limit, offset = normalize_pagination(limit, offset)
    query = select(Customer).order_by(Customer.id).limit(limit).offset(offset)
    return g.db.execute(query).scalars().all()

