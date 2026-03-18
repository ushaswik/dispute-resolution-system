"""
Policy Agent - REST API Server
RAG-based policy retrieval for dispute resolution
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from policy_retriever import PolicyRetriever
import uvicorn

app = FastAPI(
    title="Policy Agent API",
    description="RAG-based policy retrieval using FAISS + Cohere re-ranking",
    version="1.0.0"
)

# Initialize retriever (loads/creates index)
print("🚀 Initializing Policy Retriever...")
retriever = PolicyRetriever()
print("✅ Policy Retriever ready!")


# ==================== REQUEST/RESPONSE MODELS ====================

class PolicyRequest(BaseModel):
    """Request model for policy retrieval"""
    case_id: str
    intent_code: str
    intent_name: str
    case_description: str
    transaction_amount: Optional[float] = None
    merchant_category: Optional[str] = None


class ApplicablePolicy(BaseModel):
    """Individual policy in response"""
    policy_id: str
    policy_section: Optional[str] = None
    relevance_score: float
    excerpt: str
    guidance: str


class PolicyResponse(BaseModel):
    """Response model for policy retrieval"""
    case_id: str
    applicable_policies: List[ApplicablePolicy]
    combined_guidance: str
    recommended_action: str  # approve|deny|escalate
    confidence: float
    missing_information: Optional[List[str]] = None
    key_considerations: Optional[List[str]] = None
    num_policies_retrieved: int
    num_policies_used: int
    retrieval_method: str
    validation_warnings: Optional[List[str]] = None


# ==================== ENDPOINTS ====================

@app.get("/")
def root():
    """Service info"""
    return {
        "service": "Policy Agent",
        "status": "healthy",
        "version": "1.0.0",
        "features": [
            "FAISS vector search",
            "Cohere re-ranking",
            "GPT-4o synthesis",
            "Hallucination prevention"
        ],
        "stats": {
            "total_policy_chunks": len(retriever.policy_chunks),
            "embedding_model": retriever.EMBEDDING_MODEL,
            "synthesis_model": retriever.SYNTHESIS_MODEL,
            "top_k_retrieval": retriever.TOP_K_RETRIEVAL,
            "top_k_final": retriever.TOP_K_FINAL,
            "similarity_threshold": retriever.SIMILARITY_THRESHOLD
        }
    }


@app.get("/health")
def health_check():
    """Kubernetes health check"""
    return {"status": "healthy"}


@app.post("/retrieve-policies", response_model=PolicyResponse)
def retrieve_policies(request: PolicyRequest):
    """
    Retrieve relevant policies for a dispute case
    
    Pipeline:
    1. Query embedding
    2. FAISS vector search (top-10)
    3. Similarity filtering (>0.65)
    4. Cohere re-ranking
    5. Keep top-7
    6. GPT synthesis
    7. Citation validation
    
    Example:
```json
    {
      "case_id": "CASE-123",
      "intent_code": "INT-11",
      "intent_name": "Lost/Stolen Card",
      "case_description": "Card stolen March 1, charge March 3",
      "transaction_amount": 245.99
    }
```
    """
    try:
        result = retriever.retrieve_policies(
            case_id=request.case_id,
            intent_code=request.intent_code,
            intent_name=request.intent_name,
            case_description=request.case_description,
            transaction_amount=request.transaction_amount,
            merchant_category=request.merchant_category
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Policy retrieval failed: {str(e)}"
        )


@app.get("/policies")
def list_policies():
    """
    List all available policies in the knowledge base
    """
    
    # Get unique policies
    unique_policies = {}
    for chunk in retriever.policy_chunks:
        policy_id = chunk["policy_id"]
        if policy_id not in unique_policies:
            unique_policies[policy_id] = {
                "policy_id": policy_id,
                "policy_name": chunk["policy_name"],
                "category": chunk["category"],
                "num_chunks": 0
            }
        unique_policies[policy_id]["num_chunks"] += 1
    
    return {
        "total_policies": len(unique_policies),
        "total_chunks": len(retriever.policy_chunks),
        "policies": list(unique_policies.values())
    }


@app.get("/stats")
def get_stats():
    """
    Get retrieval statistics
    """
    return {
        "index_stats": {
            "total_chunks": len(retriever.policy_chunks),
            "embedding_dimension": retriever.embeddings.shape[1] if retriever.embeddings is not None else 0,
            "index_type": "FAISS IndexFlatIP (cosine similarity)"
        },
        "retrieval_config": {
            "embedding_model": retriever.EMBEDDING_MODEL,
            "synthesis_model": retriever.SYNTHESIS_MODEL,
            "chunk_size": retriever.CHUNK_SIZE,
            "chunk_overlap": retriever.CHUNK_OVERLAP,
            "top_k_retrieval": retriever.TOP_K_RETRIEVAL,
            "top_k_final": retriever.TOP_K_FINAL,
            "similarity_threshold": retriever.SIMILARITY_THRESHOLD
        },
        "cost_estimates": {
            "embedding_per_query": "$0.00001",
            "rerank_per_query": "$0.0001",
            "synthesis_per_query": "$0.002",
            "total_per_query": "~$0.002"
        }
    }


# ==================== RUN SERVER ====================

if __name__ == "__main__":
    print("=" * 80)
    print("🚀 POLICY AGENT API SERVER")
    print("=" * 80)
    print()
    print("Features:")
    print("  ✅ FAISS vector search")
    print("  ✅ Cohere re-ranking")
    print("  ✅ GPT-4o synthesis")
    print("  ✅ Hallucination prevention")
    print()
    print(f"Knowledge Base:")
    print(f"  📚 {len(retriever.policy_chunks)} policy chunks indexed")
    print(f"  🔍 Embedding model: {retriever.EMBEDDING_MODEL}")
    print(f"  🧠 Synthesis model: {retriever.SYNTHESIS_MODEL}")
    print()
    print("Starting server...")
    print("  Local:   http://localhost:8082")
    print("  Docs:    http://localhost:8082/docs")
    print("  Health:  http://localhost:8082/health")
    print()
    print("=" * 80)
    print()
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8082,  # Different port (Intent=8080, Document=8081, Policy=8082)
        reload=False  # Disable reload for production
    )