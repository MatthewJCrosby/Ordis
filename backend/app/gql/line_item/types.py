from .. import schema
import magql

GQLLineItem = magql.Object("LineItem", fields={
    "id": "ID!",
    "order": "Order!",
    "product": "Product!",
    "qty": "Int!",

})