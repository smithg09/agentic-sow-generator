import json
import re
from services.llm_service import llm_service
from prompts.templates import drafting_prompt_template, drafting_chat_prompt
from services.vector_service import vector_service

class DraftingAgent:
    def __init__(self):
        pass
    
    def extract_raw_json(self, response_text):
        """
        Extracts and parses raw JSON from an AI response wrapped in ```json ... ```
        or returns the raw JSON directly if no wrapping exists.
        """
        # Pattern to capture content between ```json ... ``` or just ```
        pattern = r"```(?:json)?\s*([\s\S]*?)```"

        match = re.search(pattern, response_text.strip())
        if match:
            raw_json_str = match.group(1)
        else:
            raw_json_str = response_text.strip()

        try:
            return json.loads(raw_json_str)
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            return None
    
    def get_relevant_context(self, query):
        """Get relevant context from vector store for the query"""
        context = vector_service.retrieve_context(query)
        return context
    
    def process_sow(self, state):
        """Process SOW drafting request"""
        # Get relevant context if not already provided
        if 'additional_context' not in state:
            context = self.get_relevant_context(state['user_query'])
            state['additional_context'] = context
            state['retryCount'] = 0
        
        # Prepare feedback instruction based on error state
        if state.get('error'):
            previous_content = state.get('sow', '')
            instruction = (f"Below is the previously generated content: {previous_content} "
                        f"The following errors were detected: {state['error']}. "
                        f"Please revise the content accordingly.")
        else:
            instruction = ""
        
        # Handle different flow types (normal or chat)
        if state.get('flow') == 'chat':
            prompt = drafting_chat_prompt.invoke({
                "user_query": state['user_query'],
                "previous_sow": state['previous_sow'],
                "feedback": instruction,
            })
            response = llm_service.invoke(prompt)
            return {'sow': response.content}
        else:
            prompt = drafting_prompt_template.invoke({
                "query": state['user_query'],
                "additional_context": state['additional_context'],
                "feedback": instruction,
                **state['query_map']
            })
            response = llm_service.invoke(prompt)
            return {'sow': response.content}