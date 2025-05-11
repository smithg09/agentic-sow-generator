from routes.sow_routes import sow_bp
from routes.chat_routes import chat_bp
from routes.feedback_routes import feedback_bp

# Export all blueprints for easy import in app.py
__all__ = ['sow_bp', 'chat_bp', 'feedback_bp']