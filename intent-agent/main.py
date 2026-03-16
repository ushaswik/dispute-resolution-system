"""
Intent Agent - REST API Server
Exposes intent classification as an HTTP endpoint
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from intent_classification import IntentClassifier
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="Intent Agent API",
    description="Classifies payment disputes into intent categories",
    version="1.0.0"
)

# Initialize classifier
classifier = IntentClassifier()

# Request model
class ClassifyRequest(BaseModel):
    case_id: str
    description: str

# Response model
class ClassifyResponse(BaseModel):
    case_id: str
    intent_code: str
    intent_name: str
    confidence: float
    reasoning: str

@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "service": "Intent Agent",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    """Health check for Kubernetes"""
    return {"status": "healthy"}

@app.post("/classify", response_model=ClassifyResponse)
def classify_dispute(request: ClassifyRequest):
    """
    Classify a payment dispute
    
    Args:
        request: ClassifyRequest with case_id and description
        
    Returns:
        ClassifyResponse with intent classification
    """
    try:
        # Classify the dispute
        result = classifier.classify(request.description)
        
        # Add case_id to result
        result["case_id"] = request.case_id
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Classification failed: {str(e)}"
        )

# Run the server
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True  # Auto-reload on code changes
    )