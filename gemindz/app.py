from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import datetime
from blueprints import register_blueprints
from database import init_db
from config import DevelopmentConfig
from error_handlers import register_error_handlers


def create_app():
    flask_app = Flask(__name__)
    flask_app.config.from_object(DevelopmentConfig)

    JWTManager(flask_app)
    init_db(flask_app)
    register_blueprints(flask_app)
    register_error_handlers(flask_app)

    flask_app.start_time = datetime.now()

    return flask_app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
