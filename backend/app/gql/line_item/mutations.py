from flask import g
from sqlalchemy import select   
from sqlalchemy.exc import IntegrityError
from app.models.line_item import LineItem
from app.models.product import Product
from app.utils import commit_or_rollback
from app.gql.utils import delete_entity, get_entity, update_entity
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
        "qty": "Int",
        "price": "Decimal"
    }
)

schema.add_type(LineItemCreateInput)
schema.add_type(LineItemUpdateInput)    

@schema.mutation.field("createLineItem", "LineItem", args={"input":"LineItemCreateInput!"})
def resolve_create_line_item(parent, info, **kwargs):
    input_data = kwargs["input"]
    product = get_entity(Product, input_data["product_id"])
    line_item_data ={
        "name": product.name,
        "description": product.description,
        "product_id": product.id,
        "price": product.price,
        **input_data
    }
    line_item = LineItem(**line_item_data)

    g.db.add(line_item)
    g.db.flush()
    line_item.order.update_total()
    commit_or_rollback("LineItem", "create")
    g.db.refresh(line_item)
    return line_item


@schema.mutation.field("updateLineItem", "LineItem", args={"id":"ID!", "input": "LineItemUpdateInput!"})
def resolve_update_line_item(parent, info, **kwargs):
    line_item_id = kwargs["id"]
    input_data = kwargs["input"]
    line_item = get_entity(LineItem, line_item_id)

    update_entity(line_item, input_data, allowed_fields=["qty", "price"])

    line_item.order.update_total()
    commit_or_rollback("LineItem", "update")
    g.db.refresh(line_item)
    return line_item


@schema.mutation.field("deleteLineItem", "Boolean!", args={"id": "ID!"})
def resolve_delete_line_item(parent, info, **kwargs):
    line_item_id = kwargs["id"]
    line_item = get_entity(LineItem, line_item_id)
    order = line_item.order

    g.db.delete(line_item)
    order.update_total()
    commit_or_rollback("LineItem", "delete")
    return True
