import click
from flask import current_app
from werkzeug.security import generate_password_hash
from app import db
from app.models.user import User, UserTypeEnum
from app.models.employee import DepartmentEnum, Employee

@click.command("create-admin")
@click.argument("first")
@click.argument("last")
@click.argument("email")
@click.argument("password")
def create_admin(first, last, email, password):
    session = db.get_session()
    if session.query(User).filter_by(email=email).first():
        click.echo(f"User with email {email} already exists.")
        return
    user = User(
        first_name=first,
        last_name=last,
        email=email,
        password_hash=generate_password_hash(password),
        is_active=True,
        is_admin=True,
        user_type=UserTypeEnum.ADMIN
    )
    employee = Employee(department=DepartmentEnum.MANAGER, user=user)
    
    session.add(user)
    session.add(employee)
    session.commit()
    click.echo(f"Admin user {email} created.")
