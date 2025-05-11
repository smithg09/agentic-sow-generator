from flask import Blueprint, request, jsonify
from graph.sow_graph import graph

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['POST'])
def chat():
    try:
        # Get the request data
        data = request.get_json()
        
        # Extract necessary fields
        user_query = data.get("message", "Unknown")
        generated_sow = data.get("context", "Unknown")
        
        # Process the chat request through the agent workflow graph
        response = graph.invoke({ 
            'user_query': user_query, 
            'flow': 'chat', 
            'previous_sow': generated_sow 
        })

        # Return the formatted response
        sow_response = {
            "status": "success",
            "message": response['formatted_sow'],
            "sow_json": response['sow'],
            "fileName": response['doc_file_path']
        }
        
        return jsonify(sow_response), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500