from .. import schema
import magql

GQLCustomer = magql.Object("Customer", fields={
    "id": "ID!",
    "user_id": "ID!",
    "user": "User",
    "orders": "[Order]",
    "created_on": "DateTime",
})

schema.add_type(GQLCustomer)