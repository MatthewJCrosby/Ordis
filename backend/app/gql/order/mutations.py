from flask import g
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.models.order import Order
from .. import schema
import magql

OrderCreateInput = magql.InputObject(
    "OrderCreateInput",
    fields={
        "customer_id": "ID!",
    }
)

OrderUpdateInput = magql.InputObject(
    "OrderUpdateInput",
    fields={
        "service_tech_id": "ID",
    }
)

schema.add_type(OrderCreateInput)
schema.add_type(OrderUpdateInput)

@schema.mutation.field("createOrder", "Order", args={"input": "OrderCreateInput!"})
def resolve_create_order(parent, info, **kwargs):
    input_data = kwargs["input"]
    order = Order(
        customer_id=input_data["customer_id"],
    )

    g.db.add(order)
    try:
        g.db.flush()
        g.db.commit()
    except IntegrityError:
        g.db.rollback()
        raise Exception("Failed to create order")
    return order

@schema.mutation.field("updateOrder", "Order", args={"id": "ID!", "input": "OrderUpdateInput!"})
def resolve_update_order(parent, info, **kwargs):
    order_id = kwargs["id"]
    input_data = kwargs["input"]
    order = g.db.execute(select(Order).where(Order.id == order_id)).scalar_one_or_none()
    if not order:
        raise Exception("Order not found")
    
    if input_data.get("service_tech_id") is not None:
        order.tech_id = input_data["service_tech_id"]
    try:
        g.db.flush()
        g.db.commit()
    except IntegrityError:
        g.db.rollback()
        raise Exception("Failed to update order")
    return order

@schema.mutation.field("deleteOrder", "Boolean!", args={"id": "ID!"})
def resolve_delete_order(parent, info, **kwargs):
    order_id = kwargs["id"]
    order = g.db.execute(select(Order).where(Order.id == order_id)).scalar_one_or_none()
    if not order:
        raise Exception("Order not found")
    g.db.delete(order)
    g.db.commit()
    return True

