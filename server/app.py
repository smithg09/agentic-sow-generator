from flask import Flask
from flask_cors import CORS
from config import POSTGRESQL_BASE_URL

from models.sow import db
from routes import sow_bp, chat_bp, feedback_bp

def create_app():
    """Application factory function to create and configure the Flask app"""
    app = Flask(__name__, static_folder='static')
    
    # Configure the application
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{POSTGRESQL_BASE_URL}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Initialize extensions
    CORS(app)  # Enable CORS to allow frontend requests
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(sow_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(feedback_bp)
    
    return app

# Initialize the database
def init_db(app):
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    # Create the application
    app = create_app()
    
    # Initialize database
    init_db(app)
    
    # Run the application
    app.run(debug=True, port=8080)
