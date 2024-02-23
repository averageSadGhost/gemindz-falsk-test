from flask import Blueprint, jsonify, request
from models import Log
from datetime import datetime

logs_bp = Blueprint('logs', __name__, url_prefix='/logs')


@logs_bp.route('/', methods=['GET'])
def get_logs():
    """
    Retrieve logs based on query parameters.

    Supported query parameters:
    - endpoint_name: Filter logs by endpoint name.
    - status_code: Filter logs by status code.
    - time[gte]: Filter logs with a timestamp greater than or equal to the provided time.
    - time[lte]: Filter logs with a timestamp less than or equal to the provided time.
    - time: Filter logs with a timestamp equal to the provided time.

    Returns:
        JSON: List of logs matching the query parameters.
    """
    query_params = request.args.to_dict()

    # Initialize the base query
    base_query = Log.query

    # Filter logs by endpoint name
    endpoint_name = query_params.get('endpoint_name')
    if endpoint_name:
        base_query = base_query.filter(Log.endpoint_name == endpoint_name)

    # Filter logs by status code
    status_code = query_params.get('status_code')
    if status_code:
        base_query = base_query.filter(Log.status_code == int(status_code))

    # Filter logs by time range
    time_gte = query_params.get('time[gte]')
    time_lte = query_params.get('time[lte]')
    time_eq = query_params.get('time')

    if time_gte:
        try:
            time_gte = datetime.fromisoformat(time_gte)
            base_query = base_query.filter(Log.created_at >= time_gte)
        except ValueError:
            return jsonify({"error": "Invalid date format for time[gte]. Please provide date in ISO 8601 format"}), 400

    if time_lte:
        try:
            time_lte = datetime.fromisoformat(time_lte)
            base_query = base_query.filter(Log.created_at <= time_lte)
        except ValueError:
            return jsonify({"error": "Invalid date format for time[lte]. Please provide date in ISO 8601 format"}), 400

    if time_eq:
        try:
            time_eq = datetime.fromisoformat(time_eq)
            base_query = base_query.filter(Log.created_at == time_eq)
        except ValueError:
            return jsonify({"error": "Invalid date format for time. Please provide date in ISO 8601 format"}), 400

    logs = base_query.all()

    # Serialize logs to JSON
    serialized_logs = [{
        'id': log.id,
        'endpoint_name': log.endpoint_name,
        'method': log.method,
        'status_code': log.status_code,
        'error': log.error,
        'created_at': log.created_at
    } for log in logs]

    return jsonify(serialized_logs), 200
