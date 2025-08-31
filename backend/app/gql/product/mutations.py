from flask import g
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.utils import commit_or_rollback
from app.gql.utils import get_entity, update_entity, delete_entity
from .. import schema
from app.models.product import Product
import magql

ProductCreateInput = magql.InputObject(
    "ProductCreateInput", 
    fields={
        "name": "String!",
        "description": "String",
        "price": "Decimal!"
    }
)

ProductUpdateInput = magql.InputObject(
    "ProductUpdateInput", 
    fields={
        "name": "String",
        "description": "String",
        "price": "Decimal"
    }
)

schema.add_type(ProductCreateInput)
schema.add_type(ProductUpdateInput)

@schema.mutation.field("createProduct", "Product", args={"input": "ProductCreateInput!"})
def resolve_create_product(parent, info, **kwargs):
    input_data = kwargs["input"]
    product = Product(**input_data)
    g.db.add(product)
    commit_or_rollback("Product", "create")

    return product


@schema.mutation.field("updateProduct", "Product", args={"id": "ID!", "input":"ProductUpdateInput"})
def resolve_update_product(parent, info, **kwargs):
    id = kwargs["id"]
    input_data = kwargs["input"]
    product = get_entity(Product, id)
    update_entity(product, input_data, allowed_fields=["name", "description", "price"])
    commit_or_rollback("Product", "update")

    return product


@schema.mutation.field("deleteProduct", "Boolean!", args={"id": "ID!"})
def resolve_delete_product(parent, info, **kwargs):
    delete_entity(Product, kwargs["id"])
    commit_or_rollback("Product", "delete")
    return True

