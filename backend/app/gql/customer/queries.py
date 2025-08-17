from flask import g
from sqlalchemy import select
from .. import schema
from app.models.customer import Customer

@schema.query.field("customer", "Customer", args={"id": "ID!"})
def resolve_customer(_, info, **kwargs):
    cid = kwargs["id"]
    return g.db.execute(
        select(Customer).where(Customer.id == cid)
    ).scalar_one_or_none()

@schema.query.field("customers", "[Customer!]")
def resolve_customers(_, info, **kwargs):
    return g.db.execute(
        select(Customer).order_by(Customer.id)
    ).scalars().all()

