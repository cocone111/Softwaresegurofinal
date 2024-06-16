from flask import Blueprint, request, jsonify
from app import db
from models import User, Inventory
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from functools import wraps

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')
inventory_blueprint = Blueprint('inventory', __name__, url_prefix='/inventory')

def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_email = get_jwt_identity()
        user = User.query.filter_by(email=user_email).first()
        if user.role != 'administrador':
            return jsonify({"msg": "Access denied"}), 403
        return fn(*args, **kwargs)
    return wrapper

def docente_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_email = get_jwt_identity()
        user = User.query.filter_by(email=user_email).first()
        if user.role not in ['administrador', 'docente']:
            return jsonify({"msg": "Access denied"}), 403
        return fn(*args, **kwargs)
    return wrapper

@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    password = data['password']
    role = data['role']
    
    if role not in ['administrador', 'docente']:
        return jsonify({"msg": "Invalid role"}), 400

    user = User(email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User registered successfully"}), 201

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200

@inventory_blueprint.route('/create', methods=['POST'])
@admin_required
def create_inventory():
    data = request.get_json()
    item_name = data['item_name']
    quantity = data['quantity']
    inventory = Inventory(item_name=item_name, quantity=quantity)
    db.session.add(inventory)
    db.session.commit()
    return jsonify({"msg": "Inventory item created successfully"}), 201

@inventory_blueprint.route('/view', methods=['GET'])
@docente_required
def view_inventory():
    inventory_items = Inventory.query.all()
    items = [{"id": item.id, "item_name": item.item_name, "quantity": item.quantity} for item in inventory_items]
    return jsonify(items), 200
