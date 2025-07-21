from ariadne import QueryType, MutationType
from app.models.customer import Customer
from ..utils.crud import (
    get_all,
    get_by_id,
    create_model,
    update_model,
    delete_model
)

query = QueryType()
mutation = MutationType()

@query.field("customers")
def resolve_customers(_, info):
    return Customer.query.all()

resolvers = [query, mutation]