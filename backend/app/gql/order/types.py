from .. import schema
import magql

GQLOrder = magql.Object("Order", fields={
    "id": "ID!",
    "customer": "Customer!",
    "line_items": "[LineItem]",
    "service_tech": "Employee",
    "total": "Decimal"

})
schema.add_type(GQLOrder)

