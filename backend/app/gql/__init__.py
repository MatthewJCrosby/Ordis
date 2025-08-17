import magql

schema = magql.Schema()

from .customer import types as _customer_types
from .customer import queries as _customer_queries
from .customer import mutations as _customer_mutations


@schema.query.field("greet", "String!", args={"name": magql.Argument("String", default="Ordis")})
def resolve_greet(parent, info, **kwargs):
    name = kwargs.pop("name")
    return f"hello, {name}!"