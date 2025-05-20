import json
import re

def extract_json(text, task):
    def clean_json(text):
            """Remove markdown JSON formatting and return a valid JSON string"""
            match = re.search(r'```json\n(.*?)\n```', text, re.DOTALL)
            if match:
                return match.group(1)  # Extract JSON part
            return text  # If no match, assume it's already clean JSON      
      
    if (task == 'responder') or (task == 'mediator'):
        def extract_reasoning(text):
            """Extract the justification from the JSON response"""
            try:
                text = clean_json(text)  # Remove ```json ... ```
                data = json.loads(text)  # Convert string to dictionary
                return data.get("justification", None)  # Safely extract justification
            except json.JSONDecodeError:
                return None  # Handle invalid JSON gracefully

        def extract_option(text):
            """Extract the selected option (A, B, or C) from the JSON response"""
            try:
                text = clean_json(text)  # Remove ```json ... ```
                data = json.loads(text)  # Convert string to dictionary
                return data.get("selected_option", None)  # Safely extract option
            except json.JSONDecodeError:
                return None  # Handle invalid JSON gracefully          
        return extract_option(text), extract_reasoning(text)
    
    elif task == 'evaluator':
        def extract_reasoning(text):
            """Extract the justification from the JSON response"""
            try:
                text = clean_json(text)  # Remove ```json ... ```
                data = json.loads(text)  # Convert string to dictionary
                return data.get("justification", None)  # Safely extract justification
            except json.JSONDecodeError:
                return None  # Handle invalid JSON gracefully

        def extract_option(text):
            """Extract the selected option (Yes or No) from the JSON response"""
            try:
                text = clean_json(text)  # Remove ```json ... ```
                data = json.loads(text)  # Convert string to dictionary
                return data.get("valid_answer", None)  # Safely extract option
            except json.JSONDecodeError:
                return None  # Handle invalid JSON gracefully          
        return extract_option(text), extract_reasoning(text)
    
    elif task=='blind_responder':

        def extract_option(text):
            """Extract the selected option (Yes or No) from the JSON response"""
            try:
                text = clean_json(text)  # Remove ```json ... ```
                data = json.loads(text)  # Convert string to dictionary
                return data.get("response", None)  # Safely extract option
            except json.JSONDecodeError:
                return None  # Handle invalid JSON gracefully          
        return extract_option(text)
    
