from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, TestCase, User

test_cases_bp = Blueprint('test_cases', __name__, url_prefix='/testcases')


@test_cases_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_test_cases():
    """
    Retrieve all test cases.

    Returns:
        JSON: A list of all test cases.
    """
    test_cases = TestCase.query.all()
    results = [{"id": test_case.id, "name": test_case.name,
                "description": test_case.description} for test_case in test_cases]
    return jsonify(results), 200


@test_cases_bp.route('/<int:test_case_id>', methods=['GET'])
@jwt_required()
def get_single_test_case(test_case_id):
    """
    Retrieve a single test case by its ID.

    Args:
        test_case_id (int): ID of the test case.

    Returns:
        JSON: Details of the requested test case.
    """
    test_case = db.session.get(TestCase, test_case_id)
    if not test_case:
        return jsonify({"error": "Test case not found"}), 404
    return jsonify({"id": test_case.id, "name": test_case.name, "description": test_case.description}), 200


@test_cases_bp.route('/', methods=['POST'])
@jwt_required()
def create_test_case():
    """
    Create a new test case.

    Returns:
        JSON: Confirmation message and details of the created test case upon successful creation.
    """
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user or user.role != 'admin':
        return jsonify({"error": "Only admins can create test cases"}), 401

    data = request.get_json()
    if not data or 'name' not in data or not isinstance(data['name'], str) or len(data['name']) > 100:
        return jsonify({"error": "Invalid name provided for test case"}), 400

    description = data.get('description', '')
    if description and not isinstance(description, str):
        return jsonify({"error": "Invalid description provided for test case"}), 400

    new_test_case = TestCase(name=data['name'], description=description)
    db.session.add(new_test_case)
    db.session.commit()

    # Return confirmation message along with the details of the created test case
    response_body = {
        "message": "Test case created successfully",
        "test_case": {
            "id": new_test_case.id,
            "name": new_test_case.name,
            "description": new_test_case.description
        }
    }
    return jsonify(response_body), 201


@test_cases_bp.route('/<int:test_case_id>', methods=['PUT'])
@jwt_required()
def update_test_case(test_case_id):
    """
    Update an existing test case.

    Args:
        test_case_id (int): ID of the test case to update.

    Returns:
        JSON: Confirmation message upon successful update.
    """
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user or user.role != 'admin':
        return jsonify({"error": "Only admins can update test cases"}), 401

    test_case = db.session.get(TestCase, test_case_id)
    if not test_case:
        return jsonify({"error": "Test case not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided for update"}), 400

    name = data.get('name', None)
    if name is None or not isinstance(name, str) or len(name) > 100:
        return jsonify({"error": "Invalid name provided for test case"}), 400

    description = data.get('description', None)
    if description is not None and not isinstance(description, str):
        return jsonify({"error": "Invalid description provided for test case"}), 400

    test_case.name = name
    test_case.description = description
    db.session.commit()

    return jsonify({"message": "Test case updated successfully"}), 200


@test_cases_bp.route('/<int:test_case_id>', methods=['DELETE'])
@jwt_required()
def delete_test_case(test_case_id):
    """
    Delete a test case.

    Args:
        test_case_id (int): ID of the test case to delete.

    Returns:
        JSON: Confirmation message upon successful deletion.
    """
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user or user.role != 'admin':
        return jsonify({"error": "Only admins can delete test cases"}), 401

    test_case = db.session.get(TestCase, test_case_id)
    if not test_case:
        return jsonify({"error": "Test case not found"}), 404

    db.session.delete(test_case)
    db.session.commit()
    return jsonify({"message": "Test case deleted successfully"}), 200
