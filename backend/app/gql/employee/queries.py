from flask import g
from sqlalchemy import select

from app.gql.utils import get_entity, get_entities
from .. import schema
from app.models.employee import Employee
from app.gql.pagination import normalize_pagination


@schema.query.field("employee", "Employee", args={"id": "ID!"})
def resolve_employee(parent, info, **kwargs):
    employee_id = kwargs["id"]
    return get_entity(Employee, employee_id)

@schema.query.field("employees", "[Employee!]", args={"limit": "Int", "offset":"Int"})
def resolve_employees(parent, info, **kwargs):
    return get_entities(Employee, **kwargs)
