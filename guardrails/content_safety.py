"""
Content Safety Checker
RUBRIC: Governance & Guardrails - Content safety checks (2 marks)

TASK: Implement keyword-based content safety checking
"""

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class ContentSafety:
    """Checks content for safety violations"""
    
    def __init__(self):
        # HINT: Define unsafe keyword patterns for different categories
        self.unsafe_patterns = {
            'violence': ___,  # HINT: List of violence-related keywords like ['kill', 'attack', etc.]
            'hate_speech': ___,  # HINT: List of hate speech keywords like
            'profanity': ___,  # HINT: List of profanity keywords
            'personal_attack': ___  # HINT: List of personal attack keywords like
        }
        
        # HINT: Define travel-specific red flags
        self.travel_red_flags = ___  # HINT: List like ['fraud', 'fake booking', 'scam', etc.]
    
    def check(self, text: str) -> Dict:
        """
        Check text for safety violations
        
        HINT: This method should:
        1. Convert text to lowercase
        2. Initialize empty flags list
        3. Check text against unsafe_patterns
        4. Check text against travel_red_flags
        5. Return dict with is_safe, flags, severity
        """
        text_lower = text.___()  # HINT: .lower()
        flags = []
        
        # HINT: Check general unsafe patterns
        for category, keywords in self.unsafe_patterns.___(): 
            for keyword in keywords:
                if keyword in ___:  
                    flags.append({
                        'category': ___,
                        'keyword': ___,   
                        'severity': '___' # HINT: 'high' for violence/hate speech, 'medium' for profanity, 'low' for personal attack
                    })
        
        # HINT: Check travel-specific red flags
        for red_flag in self.___: 
            if red_flag in text_lower:
                flags.append({
                    'category': '___', 
                    'keyword': ___,  
                    'severity': '___' 
                })
        
        return {
            'is_safe': ___, 
            'flags': ___,    
            'severity': ___  
        }
    
    def get_safety_score(self, text: str) -> float:
        """
        Calculate safety score (0-1)
        
        HINT: Return 1.0 if safe, otherwise reduce by 0.2 per flag (minimum 0.0)
        """
        result = self.___(text) 
        
        if result['___']:  
            return ___ 
        
        # HINT: Reduce score based on violations
        penalty = ___ * len(result['flags'])  
        return max(___, 1.0 - penalty) 