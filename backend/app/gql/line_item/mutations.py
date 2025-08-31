from flask import g
from sqlalchemy import select   
from sqlalchemy.exc import IntegrityError
from app.models.line_item import LineItem
from app.models.product import Product
from .. import schema
import magql

LineItemCreateInput = magql.InputObject(
    "LineItemCreateInput",
    fields={
        "product_id": "ID!",
        "qty": "Int!",
        "order_id": "ID!",

    }
)

LineItemUpdateInput = magql.InputObject(
    "LineItemUpdateInput",
    fields={
        "product_id": "ID",
        "qty": "Int",
        "order_id": "ID",
    }
)

schema.add_type(LineItemCreateInput)
schema.add_type(LineItemUpdateInput)    

@schema.mutation.field("createLineItem", "LineItem", args={"input":"LineItemCreateInput!"})
def resolve_create_line_item(parent, info, **kwargs):
    input_data = kwargs["input"]
    product = g.db.execute(select(Product).where(Product.id == input_data["product_id"])).scalar_one_or_none()
    if not product:
        raise Exception("Product not found")

    line_item = LineItem(
        name = product.name,
        description = product.description,
        product_id=product.id,
        price=product.price,
        qty=input_data["qty"],
        order_id=input_data["order_id"],
    )
    g.db.add(line_item)
    line_item.order.update_total()

    try:
        g.db.flush()
        g.db.commit()
    except IntegrityError:
        g.db.rollback()
        raise Exception("Failed to create line item")
    return line_item

@schema.mutation.field("updateLineItem", "LineItem", args={"id":"ID!", "input": "LineItemUpdateInput!"})
def resolve_update_line_item(parent, info, **kwargs):
    line_item_id = kwargs["id"]
    input_data = kwargs["input"]
    line_item = g.db.execute(select(LineItem).where(LineItem.id == line_item_id)).scalar_one_or_none()
    if not line_item:
        raise Exception("Line item not found")

    if input_data.get("product_id"):
        line_item.product_id = input_data["product_id"]
    if input_data.get("qty"):
        line_item.qty = input_data["qty"]

    line_item.order.update_total()
    try:
        g.db.flush()
        g.db.commit()
    except IntegrityError:
        g.db.rollback()
        raise Exception("Failed to update line item")
    return line_item

@schema.mutation.field("deleteLineItem", "Boolean!", args={"id": "ID!"})
def resolve_delete_line_item(parent, info, **kwargs):
    line_item_id = kwargs["id"]
    line_item = g.db.execute(select(LineItem).where(LineItem.id == line_item_id)).scalar_one_or_none()
    if not line_item:
        raise Exception("Line item not found")
    order = line_item.order
    g.db.delete(line_item)
    order.update_total()
    try:
        g.db.flush()
        g.db.commit()
    except IntegrityError:
        g.db.rollback()
        raise Exception("Failed to delete line item")
    return True