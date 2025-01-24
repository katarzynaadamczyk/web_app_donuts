from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import logging
from logging.handlers import RotatingFileHandler
import os
from werkzeug.exceptions import HTTPException, NotFound

db = SQLAlchemy()


def create_app():
    '''
    function returning Flask application
    '''
    # initialize Flask app
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    db.init_app(app)
    app.db = db

    # register routes blueprint
    from .routes import main
    app.register_blueprint(main)

    # create ./logs path if not existing
    if not os.path.exists('./logs'):
        os.makedirs('./logs')
    logger = logging.getLogger('app')

    # create logging handler
    if not logger.handlers:
        handler = RotatingFileHandler(
            "./logs/app.log", maxBytes=1000000, backupCount=5
        )
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)
    app.logger.propagate = False

    # global error handling
    # handling HTTP exception
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        app.logger.error(f"HTTP Exception: {e.description}")
        return jsonify({
            "error": e.description,
            "code": e.code
        }), e.code

    # handling 404 (NotFound) exception
    @app.errorhandler(NotFound)
    def handle_404_error(e):
        app.logger.error(f"404 Error: {e.description}")
        return jsonify({
            "error": "Resource not found",
            "code": e.code
        }), e.code

    # handling unexpected errors
    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        app.logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return jsonify({
            "error": "An unexpected error occurred.",
            "code": 500
        }), 500

    return app
