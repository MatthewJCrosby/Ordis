from flask import g
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from .. import schema
from app.models.employee import Employee
import magql


EmployeeCreateInput = magql.InputObject(
    "EmployeeCreateInput",
    fields={
        "name": "String!",
        "department": "String!",
    }
)
EmployeeUpdateInput = magql.InputObject(
    "EmployeeUpdateInput",
    fields={
        "name": "String",
        "department": "String",
    }
)

schema.add_type(EmployeeCreateInput)
schema.add_type(EmployeeUpdateInput)

@schema.mutation.field("createEmployee", "Employee", args={"input": "EmployeeCreateInput!"})
def resolve_create_employee(parent, info, **kwargs):
    input = kwargs["input"]
    name = (input.get("name") or "").strip()
    department = (input.get("department") or "").strip()

    if not name or not department:
        raise ValueError("Name and department are required!")
    
    employee = Employee(name=name, department=department)
    g.db.add(employee)
    g.db.flush()
    return employee

@schema.mutation.field("updateEmployee", "Employee", args={"id": "ID!", "input":"EmployeeUpdateInput"})
def resolve_employee_update(parent, info, **kwargs):
    input = kwargs["input"]
    employee_id = kwargs["id"]
    employee = g.db.execute(select(Employee).where(Employee.id == employee_id)).scalar_one_or_none()
    if not employee:
        raise ValueError("Employee not found")
    if input.get("name") is not None:
        employee.name = (input["name"] or "").strip()
    if input.get("department") is not None:
        employee.department = (input["department"] or "").strip()
    g.db.add(employee)
    g.db.flush()
    return employee


@schema.mutation.field("deleteEmployee", "Boolean!", args={"id": "ID!"})
def resolve_employee_delete(parent, info, **kwargs):
    employee_id = kwargs["id"]
    employee = g.db.execute(select(Employee).where(Employee.id == employee_id)).scalar_one_or_none()
    if not employee:
        raise ValueError("Employee not found")
    g.db.delete(employee)
    g.db.flush()
    return True
