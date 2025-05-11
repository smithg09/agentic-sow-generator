from flask import Blueprint, request, jsonify
from services.vector_service import vector_service

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/like-sow', methods=['POST'])
def like_sow():
    try:
        # Get the request data
        data = request.get_json()
        
        # Extract the SOW content
        sow_content = data.get("content", "Unknown")

        # Store the SOW content in the vector database
        doc_id = vector_service.store_document(sow_content, "user_generated_sow")

        return jsonify({
            "status": "success", 
            "message": "SOW liked and stored successfully.",
            "doc_id": doc_id
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500