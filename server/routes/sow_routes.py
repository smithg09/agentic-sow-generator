from flask import Blueprint, request, jsonify
from models.sow import db, SOWUserInput
from graph.sow_graph import graph

sow_bp = Blueprint('sow', __name__)

@sow_bp.route('/generate-sow', methods=['POST'])
def generate_sow():
    try:
        # Get the request data
        data = request.get_json()
        
        # Extract necessary fields
        project_objectives = data.get("projectObjectives", "NA")
        project_scope = data.get("projectScope", "NA")
        detailed_desc = data.get("servicesDescription", "NA")
        specific_feature = data.get("specificFeatures", "NA")
        platform_tech = data.get("platformsTechnologies", "NA")
        integrations = data.get("integrations", "NA")
        design_specification = data.get("designSpecifications", "NA")
        out_of_scope = data.get("outOfScope", "NA")
        deliverables = data.get("deliverables", "NA")
        project_timeline = data.get("timeline", "NA")
        

        # Store user's query in database for future use
        sow_data = SOWUserInput(
                                project_objectives=project_objectives,
                                project_scope=project_scope,
                                detailed_desc= detailed_desc,
                                specific_feature=specific_feature,
                                platform_tech=platform_tech,
                                integrations=integrations,
                                design_specification=design_specification,
                                out_of_scope=out_of_scope,
                                deliverables=deliverables,
                                project_timeline=project_timeline)
        db.session.add(sow_data)
        db.session.commit()

        # Prepare the user query and query map
        user_query = (
            f"Objectives of project are {project_objectives}.\n"
            f"Scope of the project is {project_scope}.\n"
            f"Detailed Description of Services is {detailed_desc}.\n"
            f"Specific Features are {specific_feature}.\n"
            f"Platforms and Technologies is {platform_tech}.\n"
            f"Integrations is {integrations}.\n"
            f"Design Specifications are {design_specification}.\n"
            f"Out of Scope is {out_of_scope}.\n"
            f"Deliverables are {deliverables}.\n"
            f"Project Timeline and Schedule is {project_timeline}."
        )
        
        user_query_map = {
            "project_objectives": project_objectives,
            "project_scope": project_scope,
            "detailed_desc": detailed_desc,
            "specific_feature": specific_feature,
            "platform_tech": platform_tech,
            "integrations": integrations,
            "design_specification": design_specification,
            "out_of_scope": out_of_scope,
            "deliverables": deliverables,
            "project_timeline": project_timeline
        }

        # Process the request through the agent workflow graph
        response = graph.invoke({ 'user_query': user_query, 'query_map': user_query_map })
        
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