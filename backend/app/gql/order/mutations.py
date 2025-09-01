from flask import g
from app.models.order import Order
from app.utils import commit_or_rollback
from app.gql.utils import get_entity, update_entity, delete_entity
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
    order = Order(**input_data)
    g.db.add(order)
    commit_or_rollback("Order", "create")

    return order

@schema.mutation.field("updateOrder", "Order", args={"id": "ID!", "input": "OrderUpdateInput!"})
def resolve_update_order(parent, info, **kwargs):
    order_id = kwargs["id"]
    input_data = kwargs["input"]
    order = get_entity(Order, order_id)
    update_entity(order, input_data, allowed_fields=["service_tech_id"])
    commit_or_rollback("Order", "update")
    g.db.refresh(order)
    return order

@schema.mutation.field("deleteOrder", "Boolean!", args={"id": "ID!"})
def resolve_delete_order(parent, info, **kwargs):
    order_id = kwargs["id"]
    order = get_entity(Order, order_id)
    g.db.delete(order)
    commit_or_rollback("Order", "delete")
    return True

