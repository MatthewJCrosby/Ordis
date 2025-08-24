import magql

schema = magql.Schema()

from .customer import types as _customer_types
from .customer import queries as _customer_queries
from .customer import mutations as _customer_mutations
from .product import types as _product_types
from .product import queries as _product_queries
from .product import mutations as _product_mutations

from .scalars import DecimalType
schema.add_type(DecimalType)


@schema.query.field("greet", "String!", args={"name": magql.Argument("String", default="Ordis")})
def resolve_greet(parent, info, **kwargs):
    name = kwargs.pop("name")
    return f"hello, {name}!"