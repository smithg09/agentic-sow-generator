from langchain_community.chat_models import AzureChatOpenAI
from config import OPENAI_API_KEY, AZURE_DEPLOYMENT_NAME, AZURE_MODEL_NAME, AZURE_API_BASE_URL

class LLMService:
    def __init__(self):
        if not (OPENAI_API_KEY or AZURE_DEPLOYMENT_NAME or AZURE_MODEL_NAME or AZURE_API_BASE_URL):
            raise ValueError("🚨 Environment variable not set! Look for .env.example file.")
        
        self.model = AzureChatOpenAI(
            model=AZURE_MODEL_NAME,
            deployment_name=AZURE_DEPLOYMENT_NAME,
            openai_api_key=OPENAI_API_KEY,
            openai_api_base=AZURE_API_BASE_URL,
            # Do not update this value unless Azure API changes it
            # This is the default value for Azure OpenAI API and Not Model
            openai_api_version="2023-05-15",
        )
    
    def invoke(self, prompt):
        """Invoke the LLM with the given prompt"""
        return self.model.invoke(prompt)
    
    def extract_json_from_sow(self, raw_sow: str) -> dict:
        """Extract JSON from SOW content using LLM"""
        extraction_prompt = (
            '''
            Extract the following fields from the given Statement of Work into a JSON object with these keys: 
            "Project Name", "End Date", "Confidentiality", "Intellectual Property", "Termination", "Project Title", 
            "Start Date", "End Date", "Project Name", "SOW Effective Date","Company Information", "Client", 
            "Agreement Date", "Client Contact", "Contact", "Services Description", "Deliverables",
            "Milestones", "Acceptance", "Personnel and Locations", "Representatives",
            "Client Representatives", "Contractor Resources", "Terms & Conditions", "Fees", "Expenses",
            "Taxes", "Conversion", "Limitation of Liability", "Service Level Agreement", "Assumptions", 
            "Scope of Work", "Change Process", "Payment Terms", "Timeline", "Company Name", "Client Name",
            ''' + raw_sow +
            "\n\nOutput the result as a valid JSON and do not format just return pure json."
        )
        response = self.model.invoke(extraction_prompt)
        try:
            import json
            sow_data = json.loads(response.content)
            return sow_data
        except Exception as e:
            raise ValueError("Failed to extract JSON from SOW content: " + str(e))

# Initialize LLM service as a singleton
llm_service = LLMService()