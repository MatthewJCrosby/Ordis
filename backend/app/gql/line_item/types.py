from .. import schema
import magql

GQLLineItem = magql.Object("LineItem", fields={
    "id": "ID!",
    "order": "Order!",
    "product": "Product!",
    "qty": "Int!",
    "name": "String!",
    "description": "String",
    "price": "Decimal!"

})

schema.add_type(GQLLineItem)