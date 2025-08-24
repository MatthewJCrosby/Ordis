from .. import schema
import magql

GQLProduct = magql.Object("Product", fields= {
    "id": "String!",
    "name": "String!",
    "description": "String",
    "price": "Decimal!"
})

schema.add_type(GQLProduct)