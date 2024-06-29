from flask import Blueprint, jsonify, request, flash, redirect
from app.model.model import User
from app import db

user_bp = Blueprint('user', __name__)


@user_bp.route('/user', methods=['GET'])
def users():
    user_list = User.query.all()
    return jsonify({user_list})  # render_template('users.html')


@user_bp.route('/user/<int:id>', methods=['GET'])
def user(id):
    user = User.query.find_unique(id)
    return jsonify({user})


@user_bp.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data:
        return jsonify({"message": "No data provided", 'error': 'No data provided'}), 400

    username = data.get('username')
    role = data.get('role')

    if not username:
        return jsonify({'error': 'Username is required'}), 400

    isUserexist = User.query.filter_by(username=username).first()

    if isUserexist:
        return jsonify({'error': 'User already exists'}), 400

    # Example: Creating a new user in the database
    new_user = User(username=username, password="user123", role=role)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201


@user_bp.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    # Example: Get data from JSON payload sent via AJAX
    data = request.get_json()
    new_username = data.get('username')

    # Example: Update user in the database (pseudo-code)
    user = User.query.get(id)
    if user:
        user.username = new_username
        db.session.commit()

    return jsonify({'message': f'User with ID {id} updated successfully', 'new_username': new_username})


@user_bp.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    # Example: Delete user from the database (pseudo-code)
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return jsonify({'message': f'User with ID {id} deleted successfully'})
