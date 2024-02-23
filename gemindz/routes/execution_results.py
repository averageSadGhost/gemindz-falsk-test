from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, ExecutionResult, TestCase, User

execution_results_bp = Blueprint('execution_results', __name__, url_prefix='/execution_results')


@execution_results_bp.route('', methods=['POST'])
@jwt_required()
def record_execution_result():
    """
    Record the execution result for a test case on a specific test asset.

    Expects a JSON payload with 'test_case_id', 'test_asset_id', and 'result' fields.
    Requires authentication and admin privileges.

    Returns:
        JSON: Confirmation message upon successful recording of execution result.
    """
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    if not user or user.role != 'admin':
        return jsonify({"error": "Unauthorized to record execution results"}), 401

    data = request.get_json()
    if not data or 'test_case_id' not in data or 'test_asset_id' not in data or 'result' not in data:
        return jsonify({"error": "Missing required fields: test_case_id, test_asset_id, result"}), 400

    test_case_id = data['test_case_id']
    test_asset_id = data['test_asset_id']
    result = data['result']

    # Check if the test_case_id is valid
    if not db.session.query(TestCase.id).filter_by(id=test_case_id).scalar():
        return jsonify({"error": "Test case not found"}), 404

    # Save the execution result to the database
    new_execution_result = ExecutionResult(test_case_id=test_case_id, test_asset_id=test_asset_id, result=result)
    db.session.add(new_execution_result)
    db.session.commit()

    # Return the created execution result in the JSON response
    return jsonify({
        "message": "Execution result recorded successfully",
        "execution_result": {
            "id": new_execution_result.id,
            "test_case_id": new_execution_result.test_case_id,
            "test_asset_id": new_execution_result.test_asset_id,
            "result": new_execution_result.result
        }
    }), 201


@execution_results_bp.route('/<int:test_asset_id>', methods=['GET'])
@jwt_required(optional=True)
def get_execution_results_for_test_asset(test_asset_id):
    """
    Retrieve the execution results for a specific test asset.

    Args:
        test_asset_id (int): ID of the test asset.

    Returns:
        JSON: Execution results for the specified test asset.
    """
    # Query the database to fetch execution results for the given test asset ID
    execution_results = ExecutionResult.query.filter_by(test_asset_id=test_asset_id).all()

    if not execution_results:
        return jsonify({"message": "No execution results found for the specified test asset"}), 404

    # Format the results
    results = [
        {
            "id": result.id,
            "test_case_id": result.test_case_id,
            "test_asset_id": result.test_asset_id,
            "result": result.result
        } for result in execution_results
    ]

    return jsonify(results), 200
