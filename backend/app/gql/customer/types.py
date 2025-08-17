from .. import schema
import magql

GQLCustomer = magql.Object("Customer", fields={
    "id": "ID!",
    "name": "String!",
    "email": "String!",
    "phone": "String!",
    "created_at": "DateTime",
})

schema.add_type(GQLCustomer)