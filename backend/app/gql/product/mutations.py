from flask import g
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from .. import schema
from app.models.product import Product
import magql

ProductCreateInput = magql.InputObject(
    "ProductCreateInput", 
    fields={
        "name": "String!",
        "description": "String",
        "price": "String!"
    }
)

ProductUpdateInput = magql.InputObject(
    "ProductUpdateInput", 
    fields={
        "name": "String",
        "description": "String",
        "price": "String"
    }
)

schema.add_type(ProductCreateInput)
schema.add_type(ProductUpdateInput)

@schema.mutation.field("createProduct", "Product", args={"input": "ProductCreateInput!"})
def resolve_create_product(parent, info, **kwargs):
    input = kwargs["input"]
    name = (input.get("name") or "").strip()
    description = (input.get("description") or "").strip()
    price = (input.get("price") or "").strip()

    if not name or not price:
        raise ValueError("Product name and price are required!")
    
    product = Product(name=name, description=description, price=price)
    g.db.add(product)
    g.db.flush()

    return product


@schema.mutation.field("updateProduct", "Product", args={"id": "ID!", "input":"ProductUpdateInput"})
def resolve_update_product(parent, info, **kwargs):
    id = kwargs["id"]
    input = kwargs["input"]
    product = g.db.execute(select(Product).where(Product.id == id)).scalar_one_or_none()
    if not product:
        raise ValueError("Product not found")
    if input["name"] is not None:
        product.name = input["name"]
    if input["description"] is not None:
        product.description = input["description"]
    if input["price"] is not None:
        product.price = input["price"]

    try:
        g.db.flush()
    except:
        g.db.rollback()
        raise ValueError("an error with one of the inputs")
    return product


@schema.mutation.field("deleteProduct", "Boolean!", args={"id": "ID!"})
def resolve_delete_product(parent, info, **kwargs):
    id = kwargs["id"]
    product = g.db.execute(select(Product).where(Product.id == id)).scalar_one_or_none()
    if not product:
        raise ValueError("Product not found")
    g.db.delete(product)
    return True

