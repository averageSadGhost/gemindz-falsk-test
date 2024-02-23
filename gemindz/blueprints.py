from routes.test_cases import test_cases_bp
from routes.execution_results import execution_results_bp
from routes.auth import auth_bp
from routes.logs import logs_bp
from routes.home import home_bp


def register_blueprints(app):
    app.register_blueprint(test_cases_bp)
    app.register_blueprint(execution_results_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(logs_bp)
    app.register_blueprint(home_bp)
