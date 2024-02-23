from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError
from flask import jsonify


def register_error_handlers(app):
    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(error):
        # Log the exception if necessary
        app.logger.error(f"An SQLAlchemy error occurred: {error}")

        # Custom error response for SQLAlchemy errors
        error_message = "An unexpected database error occurred. Please try again later."
        return jsonify({"error": error_message}), 500

    @app.errorhandler(InternalServerError)
    def handle_internal_server_error(error):
        # Log the exception if necessary
        app.logger.error(f"An internal server error occurred: {error}")

        # Custom error response for internal server errors
        error_message = "An internal server error occurred. Please try again later."
        return jsonify({"error": error_message}), 500

    # Generic error handler for other exceptions
    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        # Log the exception if necessary
        app.logger.error(f"An error occurred: {error}")

        # Default error response
        error_message = "An unexpected error occurred. Please try again later."
        return jsonify({"error": error_message}), 500




