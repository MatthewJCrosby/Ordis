from flask import g
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.utils import commit_or_rollback
from app.gql.utils import get_entity, update_entity
from .. import schema
from app.models.customer import Customer
import magql

CustomerCreateInput = magql.InputObject(
    "CustomerCreateInput", 
    fields={
    "first_name": "String!",
    "last_name": "String!",
    "email": "String!",
    "phone": "String"
    },
)

CustomerUpdateInput = magql.InputObject(
    "CustomerUpdateInput", fields={
    "first_name": "String",
    "last_name": "String",
    "email": "String",
    "phone": "String",
    },
)

schema.add_type(CustomerCreateInput)
schema.add_type(CustomerUpdateInput)

@schema.mutation.field("createCustomer", "Customer", args={"input": "CustomerCreateInput!"})
def resolve_create_customer(parent, info, **kwargs):
    input_data = kwargs["input"]

    customer = Customer(**input_data)
    g.db.add(customer)
    commit_or_rollback("Customer", "create")
    return customer

@schema.mutation.field("updateCustomer", "Customer", args={"id": "ID!", "input":"CustomerUpdateInput!"})
def resolve_update_customer(parent, info, **kwargs):
    id = kwargs["id"]
    input_data = kwargs["input"]
    customer =  get_entity(Customer, id)

    update_entity(customer, input_data, allowed_fields=["first_name", "last_name", "email", "phone"])
    commit_or_rollback("Customer", "update")

    return customer

@schema.mutation.field("deleteCustomer", "Boolean!", args={"id":"ID!"})
def resolve_delete_customer(parent, info, **kwargs):
    id = kwargs["id"]
    customer = get_entity(Customer, id)

    g.db.delete(customer)
    commit_or_rollback("Customer", "delete")

    return True
    


    
