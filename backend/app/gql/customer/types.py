from .. import schema
import magql

GQLCustomer = magql.Object("Customer", fields={
    "id": "ID!",
    "first_name": "String!",
    "last_name": "String!",
    "email": "String!",
    "created_on": "DateTime",
})

schema.add_type(GQLCustomer)