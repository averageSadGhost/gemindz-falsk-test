from flask import Blueprint, jsonify
from datetime import datetime

home_bp = Blueprint('home', __name__)

# Store the server start time in the application instance
start_time = datetime.now()


@home_bp.route('/')
def home():
    # Calculate the uptime by subtracting the start time from the current time
    uptime = datetime.now() - start_time

    # Return the uptime in the response
    return jsonify({"message": f"The server is up and running for {uptime}"})
