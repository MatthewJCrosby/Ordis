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

CustomerUpdateInput = magql.InputObject(
    "CustomerUpdateInput", fields={
    "first_name": "String",
    "last_name": "String",
    "email": "String",
    },
)

schema.add_type(CustomerCreateInput)
schema.add_type(CustomerUpdateInput)

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

@schema.mutation.field("updateCustomer", "Customer", args={"id": "ID!", "input":"CustomerUpdateInput!"})
def resolve_update_customer(_, info, *, id, input):
    c =  g.db.execute(select(Customer).where(Customer.id == id)).scalar_one_or_none()
    if not c:
        raise ValueError("Customer not found")
    if input["first_name"] is not None:
        c.first_name = input["first_name"]
    if input["last_name"] is not None:
        c.last_name = input["last_name"]
    if "email" in input:
        c.email = input["email"]

    try:
        g.db.flush()
    except IntegrityError as e:
        g.db.rollback()

        raise ValueError("email already in use")
    return c




@schema.mutation.field("deleteCustomer", "Boolean!", args={"id":"ID!"})
def resolve_delete_customer(_, infor, *, id):
    c = g.db.execute(select(Customer).where(Customer.id == id)).scalar_one_or_none()
    if not c:
        return False
    
    g.db.delete(c)
    return True
    


    
