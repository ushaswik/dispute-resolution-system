"""
Intent Classifier Agent
Classifies payment disputes into predefined categories using GPT-4o-mini
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from the script directory
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

class IntentClassifier:
    def __init__(self):
        """Initialize the OpenAI client"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"
        
        # Define intent categories
        self.intent_categories = {
            "INT-01": "Fraudulent Transaction",
            "INT-02": "Item Not Received",
            "INT-03": "Item Not As Described",
            "INT-04": "Canceled Recurring Transaction",
            "INT-05": "Duplicate Processing",
            "INT-06": "Incorrect Transaction Amount",
            "INT-07": "Credit Not Processed",
            "INT-11": "Lost/Stolen Card",
            "INT-18": "Other/Unclassified"
        }
    
    def classify(self, case_description: str) -> dict:
        """
        Classify a dispute case into an intent category
        
        Args:
            case_description: Text description of the dispute
            
        Returns:
            dict: {
                "intent_code": str,
                "intent_name": str,
                "confidence": float,
                "reasoning": str
            }
        """
        
        # Build prompt
        prompt = self._build_prompt(case_description)
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at classifying payment disputes. Always respond in valid JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,  # Lower temperature for more consistent results
                response_format={"type": "json_object"}  # Force JSON response
            )
            
            # Parse response
            result = eval(response.choices[0].message.content)
            
            # Validate result
            return self._validate_result(result)
            
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            raise
    
    def _build_prompt(self, case_description: str) -> str:
        """Build the classification prompt"""
        
        categories_text = "\n".join([
            f"{code}: {name}" 
            for code, name in self.intent_categories.items()
        ])
        
        prompt = f"""
Classify the following payment dispute into ONE of these categories:

{categories_text}

Dispute description: "{case_description}"

Return a JSON object with these fields:
{{
    "intent_code": "the category code (e.g., INT-01)",
    "intent_name": "the category name",
    "confidence": a number between 0.0 and 1.0 indicating your confidence,
    "reasoning": "brief explanation of why you chose this category"
}}

Rules:
- If the cardholder mentions card was stolen or lost, use INT-11
- If they mention fraud or unauthorized, use INT-01
- If they mention not receiving an item, use INT-02
- If unsure, use INT-18 (Other) with lower confidence
"""
        return prompt
    
    def _validate_result(self, result: dict) -> dict:
        """Validate and clean the result"""
        
        required_fields = ["intent_code", "intent_name", "confidence", "reasoning"]
        
        # Check all required fields exist
        for field in required_fields:
            if field not in result:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate intent code
        if result["intent_code"] not in self.intent_categories:
            raise ValueError(f"Invalid intent_code: {result['intent_code']}")
        
        # Validate confidence is between 0 and 1
        if not 0.0 <= result["confidence"] <= 1.0:
            raise ValueError(f"Confidence must be between 0 and 1, got: {result['confidence']}")
        
        return result


# Test function
if __name__ == "__main__":
    # Create classifier
    classifier = IntentClassifier()
    
    # Test cases
    test_cases = [
        "My card was stolen on March 1st. I see a charge from Amazon on March 3rd for $245.99 that I didn't make.",
        "I ordered a laptop from BestBuy but never received it. They charged me $899.",
        "I canceled my Netflix subscription but they still charged me $15.99 this month.",
    ]
    
    print("Testing Intent Classifier...\n")
    
    for i, description in enumerate(test_cases, 1):
        print(f"Test Case {i}:")
        print(f"Description: {description}")
        
        result = classifier.classify(description)
        
        print(f"Result: {result['intent_code']} - {result['intent_name']}")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"Reasoning: {result['reasoning']}")
        print("-" * 80)
        print()