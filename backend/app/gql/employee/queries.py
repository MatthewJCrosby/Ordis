from flask import g
from sqlalchemy import select
from .. import schema
from app.models.employee import Employee
from app.gql.pagination import normalize_pagination


@schema.query.field("employee", "Employee", args={"id": "ID!"})
def resolve_employee(parent, info, **kwargs):
    employee_id = kwargs["id"]
    return g.db.execute(
        select(Employee).where(Employee.id == employee_id)
    ).scalar_one_or_none()

@schema.query.field("employees", "[Employee!]", args={"limit": "Int", "offset":"Int"})
def resolve_employees(parent, info, **kwargs):
    limit, offset = normalize_pagination(kwargs.get("limit"), kwargs.get("offset"))
    query = select(Employee).order_by(Employee.id).limit(limit).offset(offset)
    return g.db.execute(query).scalars().all()
