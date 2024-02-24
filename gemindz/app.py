from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
from datetime import datetime
from blueprints import register_blueprints
from database import init_db
from config import DevelopmentConfig
from models import Log
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError


def create_app():
    flask_app = Flask(__name__)
    flask_app.config.from_object(DevelopmentConfig)

    # Register JWT manager
    JWTManager(flask_app)

    # Initialize database
    init_db(flask_app)

    # Register blueprints
    register_blueprints(flask_app)

    # Register after request function

    @flask_app.after_request
    def after_request_func(response):
        # Log request details
        Log.log_request(endpoint=request.path, method=request.method,
                        status_code=response.status_code, error=None)
        return response

    # Error handler for SQLAlchemy errors
    @flask_app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(error):
        # Log the exception
        flask_app.logger.error(f"An SQLAlchemy error occurred: {error}")

        # Custom error response for SQLAlchemy errors
        error_message = "An unexpected database error occurred. Please try again later."
        return jsonify({"error": error_message}), 500

    # Error handler for internal server errors
    @flask_app.errorhandler(InternalServerError)
    def handle_internal_server_error(error):
        # Log the exception
        flask_app.logger.error(f"An internal server error occurred: {error}")

        # Custom error response for internal server errors
        error_message = "An internal server error occurred. Please try again later."
        return jsonify({"error": error_message}), 500

    # Generic error handler for other exceptions
    @flask_app.errorhandler(Exception)
    def handle_generic_exception(error):
        # Log the exception
        flask_app.logger.error(f"An error occurred: {error}")

        # Default error response
        error_message = "An unexpected error occurred. Please try again later."
        return jsonify({"error": error_message}), 500

    flask_app.start_time = datetime.now()

    return flask_app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
