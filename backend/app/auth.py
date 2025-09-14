from flask import Blueprint, make_response, request, jsonify, g
from sqlalchemy import func, text
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, jwt_required, get_jwt_identity, set_access_cookies, set_refresh_cookies
from app.models.user import User, UserTypeEnum
from app.models.employee import Employee, DepartmentEnum
from app import db
from app.models.customer import Customer
from app.models import user
from app.models.token_blacklist import TokenBlacklist

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
@jwt_required(optional=True)
def register():
    data = request.get_json()
    user_type = UserTypeEnum(data.get('user_type', 'Customer'))

    if user_type == UserTypeEnum.EMPLOYEE or user_type == UserTypeEnum.ADMIN:
        current_user_id = get_jwt_identity()
        if not current_user_id or not g.db.query(User).filter_by(id=current_user_id, is_admin=True).first():
            return jsonify({"message": "Admin privileges required to create this user type"}), 403
        
    is_admin = user_type == UserTypeEnum.ADMIN
    user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        is_active=True,
        is_admin=is_admin,
        user_type=user_type
    )

    if g.db.query(User).filter_by(email=user.email).first():
        return jsonify({"message": "User with this email already exists"}), 400
    g.db.add(user)
    g.db.flush()  # Flush to get user ID

    if user.user_type == UserTypeEnum.CUSTOMER:
        profile = Customer(user=user)
        g.db.add(profile)


    if user.user_type == UserTypeEnum.EMPLOYEE:
        profile = Employee(user_id = user.id, department=DepartmentEnum(data.get('department', 'DepartmentEnum.CUSTOMER_SERVICE.value')))
        g.db.add(profile)

    g.db.commit()
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = g.db.query(User).filter_by(email=data['email']).first()

    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    

    resp = jsonify({"msg": "Login successful"})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=str(user_id))
    return jsonify(access_token=access_token)

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    token_id = get_jwt()['jti']
    if not g.db.query(TokenBlacklist).filter_by(jti=token_id).first():
        g.db.add(TokenBlacklist(jti=token_id))
        g.db.commit()
    resp = make_response(jsonify({"msg": "Successfully logged out"}))
    resp.set_cookie("access_token", "", expires=0)
    resp.set_cookie("refresh_token", "", expires=0)
    return resp, 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = g.db.query(User).get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    return jsonify({
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "user_type": user.user_type,
        "is_admin": user.is_admin,
        "is_active": user.is_active,
        "created_on": user.created_on,
        "last_login": user.last_login
    })