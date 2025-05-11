from transformers import pipeline
import json
from services.llm_service import llm_service

class ValidationAgent:
    def __init__(self):
        self.toxicity_classifier = pipeline(
            "text-classification", 
            model="unitary/unbiased-toxic-roberta"
        )

    def validate_text(self, text, threshold=0.75):
        """Check text for toxic content"""
        try:
            result = self.toxicity_classifier(text)[0]
        except Exception as e:
            return text, None
        
        toxic_labels = [
            "toxicity", "severe_toxicity", "obscene", "threat",
            "insult", "identity_attack", "sexual_explicit"
        ]
        
        if result['label'] in toxic_labels and result['score'] > threshold:
            error_msg = (f"[⚠ TOXIC CONTENT DETECTED] Text validation failed: {text}. "
                        f"Reason: {result['label']} with score {round(result['score']*100, 2)}%")
            print(error_msg)
            return text, error_msg
            
        return text, None

    def validate_sow_data(self, sow_data):
        """Validate SOW data for toxic content"""
        validated_data = {}
        errors = {}
        
        for key, value in sow_data.items():
            if isinstance(value, dict):
                validated_subsection = {}
                subsection_errors = {}
                
                for subkey, subvalue in value.items():
                    valid_text, error = self.validate_text(subvalue)
                    validated_subsection[subkey] = valid_text
                    
                    if error:
                        subsection_errors[subkey] = error
                
                validated_data[key] = validated_subsection
                
                if subsection_errors:
                    errors[key] = subsection_errors
            else:
                valid_text, error = self.validate_text(value)
                validated_data[key] = valid_text
                
                if error:
                    errors[key] = error
                    
        return validated_data, errors

    def process_sow(self, state):
        """Process SOW for validation"""
        try:
            try:
                sow_data = json.loads(state['sow'])
            except Exception as parse_error:
                sow_data = llm_service.extract_json_from_sow(state['sow'])

            validated_data, errors = self.validate_sow_data(sow_data)
            
            if errors:
                state['error'] = json.dumps(errors)
                return {'feedback': 'REJECTED', 'retryCount': state['retryCount'] + 1}
            else:
                state['validated_sow'] = validated_data
                state.pop('error', None)
                return {'feedback': 'ACCEPTED', 'validated_sow': validated_data}
                
        except Exception as e:
            state['error'] = str(e)
            return {'feedback': 'REJECTED', 'retryCount': state['retryCount'] + 1}