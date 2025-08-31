from flask import g
from sqlalchemy import select

from app.gql.utils import get_entities, get_entity
from .. import schema
from app.models.customer import Customer
from app.gql.pagination import normalize_pagination

@schema.query.field("customer", "Customer", args={"id": "ID!"})
def resolve_customer(parent, info, **kwargs):
    customer_id = kwargs["id"]
    return get_entity(Customer, customer_id)

@schema.query.field("customers", "[Customer!]", args={"limit": "Int", "offset": "Int"})
def resolve_customers(parent, info, **kwargs):
    return get_entities(Customer, **kwargs)

