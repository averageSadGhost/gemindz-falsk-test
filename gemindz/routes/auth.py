from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from models import db, User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate user and generate access token upon successful login.

    Expects a JSON payload with 'username' and 'password' fields.

    Returns:
        JSON: Access token if login is successful.
    """
    data = request.get_json()
    if not all(key in data for key in ['username', 'password']):
        return jsonify({"error": "Username and password are required fields"}), 400

    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.

    Expects a JSON payload with 'username', 'password', and 'role' fields.

    Returns:
        JSON: Success message upon successful user registration.
    """
    data = request.get_json()
    if not all(key in data for key in ['username', 'password', 'role']):
        return jsonify({"error": "Username, password, and role are required fields"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 400

    if data['role'] not in ['admin', 'user']:
        return jsonify({"error": "Role must be 'admin' or 'user'"}), 400

    new_user = User(username=data['username'], password=data['password'], role=data['role'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201
