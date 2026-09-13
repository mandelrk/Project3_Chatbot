"""
Safety Validator
RUBRIC: Governance & Guardrails - Safety validator with Azure Content Safety (3 marks)

TASK: Implement safety validation using both local checks and Azure Content Safety
"""
import re
from typing import Dict, Any, List
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions
from src.config import Config
from guardrails.content_safety import ContentSafety

class SafetyValidator:
    """Validates content safety and detects adversarial attacks (jailbreaks)"""
    
    def __init__(self):
        # HINT: Initialize local content safety checker
        self.content_safety = ___()
        
        # HINT: Define prompt injection patterns
        self.injection_patterns = [
            r"___",  # HINT: ["ignore previous instructions", "bypass safety", "override guidelines", "you are now in developer mode", "delete all data", etc.]
            r"___",  
            r"___",  
            r"___",  
            r"___",  
            r"___",  
        ]
        
        # HINT: Initialize Azure Content Safety client if credentials available
        self.client = None
        if Config.___ and Config.___:
            try:
                self.client = ContentSafetyClient(
                    endpoint=Config.___,  
                    credential=AzureKeyCredential(Config.___)
                )
            except Exception as e:
                print(f"Warning: Failed to init Azure Content Safety: {e}")

    def validate(self, text: str, severity_threshold: str = "high") -> Dict[str, Any]:
        """
        Validates the text for safety violations
        
        HINT: This method should:
        1. Initialize flags list and is_safe boolean
        2. Run local content safety check
        3. Check for prompt injection patterns
        4. Run Azure Content Safety check if client available
        5. Return dict with is_safe, flags, severity
        """
        flags = []
        is_safe = ___ 
        
        # HINT: 1. Local Content Safety Guardrail (Keywords & Regex)
        local_result = self.content_safety.___(text) 
        if not local_result['___']:  
            is_safe = ___  # HINT: False
            for flag in local_result['___']:  # HINT: 'flags'
                flags.append(f"Unsafe Keyword ({flag['___']}): {flag['___']}")

        # HINT: 2. Specific Injection Checks
        for pattern in self.___: 
            if re.search(pattern, text, re.___): 
                is_safe = ___  
                flags.append(f"Prompt Injection Detected: {pattern}")
        
        # HINT: 3. Azure Content Safety Check
        if self.client:
            try:
                request = ___(text=text)  
                response = self.client.___(request)
                
                # HINT: Check categories_analysis for high severity flags (severity > 2)
                if response.___:  
                    for analysis in response.categories_analysis:
                        if analysis.___ > ___: 
                            is_safe = ___ 
                            flags.append(f"Azure Content Safety Violation: {analysis.___} ({analysis.___})")  # HINT: category, severity
                    
            except HttpResponseError as e:
                print(f"Azure Content Safety check failed: {e}")
        
        return {
            'is_safe': ___,  
            'flags': ___,   
            'severity': ___ if not is_safe else ___ 
        }