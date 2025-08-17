import magql

schema = magql.Schema()

from .customer import types as _customer_types
from .customer import queries as _customer_queries

