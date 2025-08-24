from .. import schema
import magql

GQLEmployee = magql.Object("Employee", fields={
    "id": "String!",
    "name": "String!",
    "department": "String!"
})

schema.add_type(GQLEmployee)