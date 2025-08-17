from flask import g
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from .. import schema
from app.models.customer import Customer
import magql

CustomerCreateInput = magql.InputObject(
    "CustomerCreateInput", 
    fields={
    "first_name": "String!",
    "last_name": "String!",
    "email": "String!",
    },
)
schema.add_type(CustomerCreateInput)

@schema.mutation.field("createCustomer", "Customer", args={"input": "CustomerCreateInput!"})
def resolve_create_customer(_, infor, input):
    first_name = (input.get("first_name") or "").strip()
    last_name = (input.get("last_name") or "").strip()
    email = (input.get("email") or "").strip()
    if not first_name or not last_name or not email:
        raise ValueError("First & Last name, email required")
    
    c = Customer(first_name=first_name, last_name=last_name, email=email)
    g.db.add(c)
    g.db.flush()

    return c

    
