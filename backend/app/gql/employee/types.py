from .. import schema
import magql

GQLEmployee = magql.Object("Employee", fields={
    "id": "String!",
    "user_id": "ID!",
    "user": "User",
    "orders": "[Order]",
    "department": "String!"
})

schema.add_type(GQLEmployee)