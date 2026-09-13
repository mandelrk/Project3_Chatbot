"""
PII Detection using regex patterns
RUBRIC: Governance & Guardrails - PII detection (2 marks)

TASK: Implement PII detection for common personally identifiable information
"""
import re
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class PIIDetector:
    """Detects Personally Identifiable Information"""
    
    def __init__(self):
        # HINT: Define regex patterns for common PII types
        # You need patterns for: email, phone, ssn, credit_card, passport, zip_code, ip_address
        self.patterns = {
            'email': r'___',  # HINT: Pattern like name@domain.com
            'phone': r'___',  # HINT: Pattern for (123) 456-7890 or 123-456-7890 format
            'ssn': r'___',  # HINT: Pattern for XXX-XX-XXXX format
            'credit_card': r'___',  # HINT: Pattern for 16 digits with optional spaces/hyphens
            'passport': r'___',  # HINT: Pattern for 1-2 letters followed by 6-9 digits
            'zip_code': r'___',  # HINT: Pattern for 5 digits or 5+4 format
            'ip_address': r'___'  # HINT: Pattern for IPv4 address (four groups of 1-3 digits)
        }
    
    def detect(self, text: str) -> Dict:
        """
        Detect PII in text
        
        HINT: This method should:
        1. Initialize empty entities list
        2. Loop through self.patterns
        3. Use re.finditer to find all matches
        4. For each match, append dict with type, value, start, end
        5. Return dict with has_pii (bool), entities (list), count (int)
        """
        entities = []
        
        # HINT: Loop through each pattern type and pattern
        for entity_type, pattern in self.patterns.___():
            # HINT: Use re.finditer to find all matches
            matches = re.___(pattern, text)
            
            for match in matches:
                # HINT: Append entity info to entities list
                entities.append({
                    'type': ___,  # HINT: entity_type
                    'value': ___,  # HINT: match.group()
                    'start': ___,  # HINT: match.start()
                    'end': ___     # HINT: match.end()
                })
        
        return {
            'has_pii': ___,  # HINT: len(entities) > 0
            'entities': ___,  # HINT: entities
            'count': ___     # HINT: len(entities)
        }
    
    def redact(self, text: str) -> str:
        """
        Redact PII from text
        
        HINT: Use re.sub to replace each pattern with [TYPE_REDACTED]
        """
        redacted_text = text
        
        # HINT: Loop through patterns and redact each type
        for entity_type, pattern in self.patterns.items():
            if entity_type == 'email':
                redacted_text = re.sub(pattern, '___', redacted_text)  # HINT: '[EMAIL_REDACTED, PHONE_REDACTED, etc.]'
            elif entity_type == 'phone':
                redacted_text = re.sub(pattern, '___', redacted_text)  
            elif entity_type == 'passport':
                redacted_text = re.sub(pattern, '___', redacted_text)  
            elif entity_type == 'credit_card':
                redacted_text = re.sub(pattern, '___', redacted_text)  
            else:
                # HINT: Use f-string to create dynamic redaction message
                redacted_text = re.sub(pattern, f'[{___}_REDACTED]', redacted_text)
        
        return redacted_text