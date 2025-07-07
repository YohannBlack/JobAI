from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    from app.routes.extract import extract_bp
    from app.routes.offres import offres_bp
    from app.routes.auth import auth_bp
    from app.routes.feedback import feedback_bp
    from app.routes.cv import cv_bp

    app.register_blueprint(extract_bp)
    app.register_blueprint(offres_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(cv_bp)

    return app
