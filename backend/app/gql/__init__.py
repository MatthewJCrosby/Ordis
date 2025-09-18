import magql

schema = magql.Schema()

from .customer import types as _customer_types
from .customer import queries as _customer_queries
from .customer import mutations as _customer_mutations
from .product import types as _product_types
from .product import queries as _product_queries
from .product import mutations as _product_mutations
from .employee import types as _employee_types
from .employee import queries as _employee_queries
from .employee import mutations as _employee_mutations  
from .order import types as _order_types
from .order import queries as _order_queries
from .order import mutations as _order_mutations
from .line_item import types as _line_item_types
from .line_item import queries as _line_item_queries
from .line_item import mutations as _line_item_mutations
from .user import types as _user_types

from .scalars import DecimalType
schema.add_type(DecimalType)


@schema.query.field("greet", "String!", args={"name": magql.Argument("String", default="Ordis")})
def resolve_greet(parent, info, **kwargs):
    name = kwargs.pop("name")
    return f"hello, {name}!"