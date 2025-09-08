from flask import g
from app.utils import commit_or_rollback
from app.gql.utils import get_entity, update_entity
from .. import schema
from app.models.employee import Employee
import magql


EmployeeCreateInput = magql.InputObject(
    "EmployeeCreateInput",
    fields={
        "department": "String!",
    }
)
EmployeeUpdateInput = magql.InputObject(
    "EmployeeUpdateInput",
    fields={
        "department": "String",
    }
)

schema.add_type(EmployeeCreateInput)
schema.add_type(EmployeeUpdateInput)

# @schema.mutation.field("createEmployee", "Employee", args={"input": "EmployeeCreateInput!"})
# def resolve_create_employee(parent, info, **kwargs):
#     input_data = kwargs["input"]
    
#     employee = Employee(**input_data)
#     g.db.add(employee)
#     commit_or_rollback("Employee", "create")
#     return employee

@schema.mutation.field("updateEmployee", "Employee", args={"id": "ID!", "input":"EmployeeUpdateInput"})
def resolve_employee_update(parent, info, **kwargs):
    input_data = kwargs["input"]
    employee_id = kwargs["id"]
    employee = get_entity(Employee, employee_id)
    
    update_entity(employee, input_data, allowed_fields=["department"])
    commit_or_rollback("Employee", "update")

    return employee


@schema.mutation.field("deleteEmployee", "Boolean!", args={"id": "ID!"})
def resolve_employee_delete(parent, info, **kwargs):
    employee_id = kwargs["id"]
    employee = get_entity(Employee, employee_id)
    g.db.delete(employee)
    commit_or_rollback("Employee", "delete")
    return True
 