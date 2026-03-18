"""
Policy Retriever - RAG Pipeline with FAISS + Cohere Re-ranking
Retrieves relevant policies for dispute resolution
"""

import os
import json
import pickle
from typing import List, Dict, Optional, Tuple
import numpy as np

# OpenAI for embeddings and synthesis
from openai import OpenAI
from dotenv import load_dotenv

# FAISS for vector search
import faiss

# Cohere for re-ranking
import cohere

# Token counting
import tiktoken

load_dotenv()


class PolicyRetriever:
    """
    RAG-based policy retrieval system
    
    Pipeline:
    1. Load policies and create chunks
    2. Generate embeddings for chunks
    3. Build FAISS index
    4. Query: embed → search → re-rank → synthesize
    """
    
    # Configuration
    CHUNK_SIZE = 700  # tokens
    CHUNK_OVERLAP = 50  # tokens
    EMBEDDING_MODEL = "text-embedding-3-small"  # Cheaper, good quality
    SYNTHESIS_MODEL = "gpt-4o-mini"
    
    SIMILARITY_THRESHOLD = 0.65  # Minimum cosine similarity
    TOP_K_RETRIEVAL = 10  # Retrieve top 10 before re-ranking
    TOP_K_FINAL = 7  # Keep top 7 after re-ranking
    
    def __init__(self):
        """Initialize APIs and load/create index"""
        
        # Initialize OpenAI
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            raise ValueError("OPENAI_API_KEY not found")
        self.openai_client = OpenAI(api_key=openai_key)
        
        # Initialize Cohere
        cohere_key = os.getenv("COHERE_API_KEY")
        if not cohere_key:
            raise ValueError("COHERE_API_KEY not found")
        self.cohere_client = cohere.Client(cohere_key)
        
        # Initialize tokenizer
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        
        # Storage
        self.policy_chunks = []  # List of chunk dicts
        self.embeddings = None   # numpy array of embeddings
        self.index = None        # FAISS index
        
        # Load or create index
        self._initialize_index()
    
    def _initialize_index(self):
        """Load existing index or create new one"""
        
        cache_path = "embeddings_cache/policy_index.pkl"
        
        if os.path.exists(cache_path):
            print("📦 Loading existing policy index...")
            self._load_index(cache_path)
            print(f"✅ Loaded {len(self.policy_chunks)} chunks")
        else:
            print("🔨 Creating new policy index...")
            self._create_index()
            self._save_index(cache_path)
            print(f"✅ Created index with {len(self.policy_chunks)} chunks")
    
    def _create_index(self):
        """Create embeddings and FAISS index from policy documents"""
        
        # Step 1: Load and chunk all policies
        print("  → Loading policies...")
        policies = self._load_policies()
        
        print(f"  → Chunking {len(policies)} policies...")
        self.policy_chunks = self._chunk_policies(policies)
        
        # Step 2: Generate embeddings
        print(f"  → Generating embeddings for {len(self.policy_chunks)} chunks...")
        self.embeddings = self._generate_embeddings(self.policy_chunks)
        
        # Step 3: Build FAISS index
        print("  → Building FAISS index...")
        self._build_faiss_index(self.embeddings)
    
    def _load_policies(self) -> List[Dict]:
        """Load all policy documents"""
        
        policies = []
        policy_dir = "policies"
        
        # Load policy index
        with open(f"{policy_dir}/policy_index.json", 'r') as f:
            policy_index = json.load(f)
        
        for policy_info in policy_index:
            filepath = f"{policy_dir}/{policy_info['filename']}"
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            policies.append({
                "policy_id": policy_info["policy_id"],
                "policy_name": policy_info["policy_name"],
                "category": policy_info["category"],
                "content": content
            })
        
        return policies
    
    def _chunk_policies(self, policies: List[Dict]) -> List[Dict]:
        """
        Chunk policies using hybrid strategy:
        1. Split by sections (semantic)
        2. If section > CHUNK_SIZE, split further
        3. Add overlap between chunks
        """
        
        all_chunks = []
        
        for policy in policies:
            # Split by sections (markdown headers)
            sections = self._split_by_sections(policy["content"])
            
            for section in sections:
                # If section small enough, keep as one chunk
                tokens = self.tokenizer.encode(section)
                
                if len(tokens) <= self.CHUNK_SIZE:
                    all_chunks.append({
                        "policy_id": policy["policy_id"],
                        "policy_name": policy["policy_name"],
                        "category": policy["category"],
                        "content": section,
                        "token_count": len(tokens)
                    })
                else:
                    # Section too large, split with overlap
                    sub_chunks = self._split_with_overlap(section, tokens)
                    
                    for sub_chunk in sub_chunks:
                        all_chunks.append({
                            "policy_id": policy["policy_id"],
                            "policy_name": policy["policy_name"],
                            "category": policy["category"],
                            "content": sub_chunk,
                            "token_count": len(self.tokenizer.encode(sub_chunk))
                        })
        
        return all_chunks
    
    def _split_by_sections(self, content: str) -> List[str]:
        """Split content by markdown headers"""
        
        lines = content.split('\n')
        sections = []
        current_section = []
        
        for line in lines:
            # New section starts with # (any level)
            if line.strip().startswith('#'):
                # Save previous section
                if current_section:
                    sections.append('\n'.join(current_section))
                # Start new section
                current_section = [line]
            else:
                current_section.append(line)
        
        # Add last section
        if current_section:
            sections.append('\n'.join(current_section))
        
        return sections
    
    def _split_with_overlap(self, text: str, tokens: List[int]) -> List[str]:
        """Split long text with overlap"""
        
        chunks = []
        start = 0
        
        while start < len(tokens):
            # Get chunk of CHUNK_SIZE tokens
            end = min(start + self.CHUNK_SIZE, len(tokens))
            chunk_tokens = tokens[start:end]
            
            # Decode back to text
            chunk_text = self.tokenizer.decode(chunk_tokens)
            chunks.append(chunk_text)
            
            # Move forward with overlap
            start += self.CHUNK_SIZE - self.CHUNK_OVERLAP
        
        return chunks
    
    def _generate_embeddings(self, chunks: List[Dict]) -> np.ndarray:
        """Generate embeddings for all chunks"""
        
        # Drop any empty/whitespace-only chunks to avoid invalid OpenAI batch input
        valid_chunks = [c for c in chunks if c["content"] and c["content"].strip()]
        if len(valid_chunks) != len(chunks):
            removed = len(chunks) - len(valid_chunks)
            print(f"    ⚠ Skipping {removed} empty/whitespace chunks before embedding")
        
        # Extract text from chunks
        texts = [chunk["content"] for chunk in valid_chunks]
        
        # Batch process (OpenAI allows up to 2048 inputs per request)
        batch_size = 100
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            
            response = self.openai_client.embeddings.create(
                model=self.EMBEDDING_MODEL,
                input=batch
            )
            
            batch_embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(batch_embeddings)
            
            print(f"    Processed {min(i + batch_size, len(texts))}/{len(texts)} chunks")
        
        return np.array(all_embeddings, dtype='float32')
    
    def _build_faiss_index(self, embeddings: np.ndarray):
        """Build FAISS index for fast similarity search"""
        
        dimension = embeddings.shape[1]  # Embedding dimension (1536 for text-embedding-3-small)
        
        # Use IndexFlatIP (Inner Product) for cosine similarity
        # Normalize embeddings first
        faiss.normalize_L2(embeddings)
        
        # Create index
        self.index = faiss.IndexFlatIP(dimension)
        
        # Add embeddings
        self.index.add(embeddings)
    
    def _save_index(self, path: str):
        """Save index to disk"""
        
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        data = {
            "policy_chunks": self.policy_chunks,
            "embeddings": self.embeddings,
            "index": faiss.serialize_index(self.index)
        }
        
        with open(path, 'wb') as f:
            pickle.dump(data, f)
    
    def _load_index(self, path: str):
        """Load index from disk"""
        
        with open(path, 'rb') as f:
            data = pickle.load(f)
        
        self.policy_chunks = data["policy_chunks"]
        self.embeddings = data["embeddings"]
        self.index = faiss.deserialize_index(data["index"])
    
    # ==================== RETRIEVAL ====================
    
    def retrieve_policies(
        self,
        case_id: str,
        intent_code: str,
        intent_name: str,
        case_description: str,
        transaction_amount: Optional[float] = None,
        merchant_category: Optional[str] = None
    ) -> Dict:
        """
        Main retrieval method
        
        Pipeline:
        1. Build query from case details
        2. Generate query embedding
        3. FAISS vector search (top-K)
        4. Filter by similarity threshold
        5. Cohere re-ranking
        6. GPT synthesis
        7. Validation
        """
        
        print(f"\n🔍 Retrieving policies for {case_id}...")
        
        # Step 1: Build query
        query = self._build_query(
            intent_name, case_description, 
            transaction_amount, merchant_category
        )
        
        # Step 2: Embed query
        print("  → Generating query embedding...")
        query_embedding = self._embed_query(query)
        
        # Step 3: Vector search
        print(f"  → Searching for top {self.TOP_K_RETRIEVAL} similar policies...")
        retrieved_chunks = self._vector_search(query_embedding, self.TOP_K_RETRIEVAL)
        
        # Step 4: Filter by threshold
        filtered_chunks = [
            chunk for chunk in retrieved_chunks 
            if chunk["similarity_score"] >= self.SIMILARITY_THRESHOLD
        ]
        
        print(f"  → Filtered to {len(filtered_chunks)} chunks (similarity > {self.SIMILARITY_THRESHOLD})")
        
        if not filtered_chunks:
            return self._no_policy_found(case_id)
        
        # Step 5: Re-rank with Cohere
        print(f"  → Re-ranking with Cohere...")
        reranked_chunks = self._rerank_with_cohere(query, filtered_chunks)
        
        # Keep top 7
        final_chunks = reranked_chunks[:self.TOP_K_FINAL]
        
        print(f"  → Using top {len(final_chunks)} chunks for synthesis")
        
        # Step 6: Synthesize with GPT
        print("  → Synthesizing guidance with GPT...")
        result = self._synthesize_guidance(
            case_id, intent_code, intent_name,
            case_description, final_chunks
        )
        
        # Step 7: Validate
        result = self._validate_result(result, final_chunks)
        
        return result
    
    def _build_query(
        self,
        intent_name: str,
        description: str,
        amount: Optional[float],
        category: Optional[str]
    ) -> str:
        """Build search query from case details"""
        
        query_parts = [
            f"Dispute type: {intent_name}",
            f"Description: {description}"
        ]
        
        if amount:
            query_parts.append(f"Transaction amount: ${amount}")
        
        if category:
            query_parts.append(f"Merchant category: {category}")
        
        return " ".join(query_parts)
    
    def _embed_query(self, query: str) -> np.ndarray:
        """Generate embedding for query"""
        
        response = self.openai_client.embeddings.create(
            model=self.EMBEDDING_MODEL,
            input=query
        )
        
        embedding = np.array([response.data[0].embedding], dtype='float32')
        faiss.normalize_L2(embedding)
        
        return embedding
    
    def _vector_search(self, query_embedding: np.ndarray, k: int) -> List[Dict]:
        """Search FAISS index"""
        
        # Search
        similarities, indices = self.index.search(query_embedding, k)
        
        # Build results
        results = []
        for i, idx in enumerate(indices[0]):
            chunk = self.policy_chunks[idx].copy()
            chunk["similarity_score"] = float(similarities[0][i])
            results.append(chunk)
        
        return results
    
    def _rerank_with_cohere(self, query: str, chunks: List[Dict]) -> List[Dict]:
        """Re-rank chunks using Cohere re-rank API"""
        
        # Prepare documents for Cohere
        documents = [chunk["content"] for chunk in chunks]
        
        try:
            # Call Cohere re-rank
            response = self.cohere_client.rerank(
                model="rerank-english-v3.0",
                query=query,
                documents=documents,
                top_n=len(documents),  # Re-rank all, we'll filter after
                return_documents=True
            )
            
            # Build reranked list
            reranked = []
            for result in response.results:
                chunk = chunks[result.index].copy()
                chunk["rerank_score"] = result.relevance_score
                reranked.append(chunk)
            
            return reranked
            
        except Exception as e:
            print(f"  ⚠ Cohere re-ranking failed: {e}")
            print("  → Falling back to vector search rankings")
            # Fallback to original order
            for chunk in chunks:
                chunk["rerank_score"] = chunk["similarity_score"]
            return chunks
    
    def _synthesize_guidance(
        self,
        case_id: str,
        intent_code: str,
        intent_name: str,
        description: str,
        chunks: List[Dict]
    ) -> Dict:
        """Use GPT to synthesize guidance from retrieved policies"""
        
        # Build context from chunks
        policy_context = self._build_policy_context(chunks)
        
        # Build prompt
        prompt = self._build_synthesis_prompt(
            intent_code, intent_name, description, policy_context
        )
        
        try:
            response = self.openai_client.chat.completions.create(
                model=self.SYNTHESIS_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert dispute resolution analyst. Provide guidance based ONLY on the provided policies. Do not make up policy numbers or guidance. Always cite policy IDs. Respond in valid JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            result = eval(response.choices[0].message.content)
            result["case_id"] = case_id
            
            return result
            
        except Exception as e:
            raise Exception(f"GPT synthesis failed: {e}")
    
    def _build_policy_context(self, chunks: List[Dict]) -> str:
        """Build context string from policy chunks"""
        
        context_parts = []
        
        for i, chunk in enumerate(chunks, 1):
            context_parts.append(f"""
Policy {i}:
Policy ID: {chunk['policy_id']}
Policy Name: {chunk['policy_name']}
Relevance Score: {chunk.get('rerank_score', chunk['similarity_score']):.2f}

Content:
{chunk['content']}

---
"""
            )
        
        return "\n".join(context_parts)
    
    def _build_synthesis_prompt(
        self,
        intent_code: str,
        intent_name: str,
        description: str,
        policy_context: str
    ) -> str:
        """Build prompt for GPT synthesis"""
        
        prompt = f"""
You are analyzing a payment dispute case. Use the provided policies to give guidance.

CASE DETAILS:
Intent Code: {intent_code}
Intent Name: {intent_name}
Description: {description}

RETRIEVED POLICIES:
{policy_context}

TASK:
Analyze the case against these policies and return a JSON object with:

{{
  "applicable_policies": [
    {{
      "policy_id": "MCD-XXXX",
      "policy_section": "Section name if identifiable",
      "relevance_score": score from retrieval (0.0-1.0),
      "excerpt": "Brief relevant excerpt from policy (2-3 sentences max)",
      "guidance": "Specific guidance this policy provides for this case"
    }}
  ],
  
  "combined_guidance": "Synthesized guidance combining all applicable policies. Be specific about what actions to take and what to check.",
  
  "recommended_action": "approve|deny|escalate",
  
  "confidence": confidence in recommendation (0.0-1.0),
  
  "missing_information": ["List any information needed to make better decision"],
  
  "key_considerations": ["Important factors to consider in this case"]
}}

CRITICAL RULES:
1. ONLY use policy IDs that appear in the retrieved policies above
2. ONLY cite information actually present in the policies
3. If no clear guidance in policies, say so (recommend escalate)
4. Quote specific policy sections when giving guidance
5. If policies conflict, note the conflict
6. Be specific: "Check if X" not just "Consider X"
"""
        
        return prompt
    
    def _validate_result(self, result: Dict, chunks: List[Dict]) -> Dict:
        """Validate that LLM didn't hallucinate policy IDs"""
        
        # Get all valid policy IDs from retrieved chunks
        valid_policy_ids = set(chunk["policy_id"] for chunk in chunks)
        
        # Check cited policies
        cited_policies = result.get("applicable_policies", [])
        
        validated_policies = []
        hallucinations = []
        
        for policy in cited_policies:
            policy_id = policy.get("policy_id")
            
            if policy_id in valid_policy_ids:
                validated_policies.append(policy)
            else:
                hallucinations.append(policy_id)
        
        # Update result
        result["applicable_policies"] = validated_policies
        
        if hallucinations:
            print(f"  ⚠ WARNING: LLM cited non-existent policies: {hallucinations}")
            result["validation_warnings"] = [
                f"LLM attempted to cite non-retrieved policy: {pid}"
                for pid in hallucinations
            ]
        
        # Add metadata
        result["num_policies_retrieved"] = len(chunks)
        result["num_policies_used"] = len(validated_policies)
        result["retrieval_method"] = "faiss_vector_search_with_cohere_rerank"
        
        return result
    
    def _no_policy_found(self, case_id: str) -> Dict:
        """Return when no relevant policies found"""
        
        return {
            "case_id": case_id,
            "applicable_policies": [],
            "combined_guidance": "No applicable policies found for this dispute type. Recommend escalation to senior analyst for manual review.",
            "recommended_action": "escalate",
            "confidence": 0.0,
            "missing_information": ["Applicable policy guidance"],
            "key_considerations": ["Case requires manual policy interpretation"],
            "num_policies_retrieved": 0,
            "num_policies_used": 0,
            "retrieval_method": "faiss_vector_search_with_cohere_rerank"
        }


# ==================== TEST FUNCTION ====================

if __name__ == "__main__":
    print("=" * 80)
    print("POLICY RETRIEVER TEST")
    print("=" * 80)
    
    # Initialize retriever (will create index if doesn't exist)
    retriever = PolicyRetriever()
    
    # Test cases
    test_cases = [
        {
            "case_id": "CASE-001",
            "intent_code": "INT-11",
            "intent_name": "Lost/Stolen Card",
            "case_description": "My card was stolen on March 1st. I see a charge from Amazon on March 3rd for $245.99 that I didn't make. I reported the card stolen on March 3rd.",
            "transaction_amount": 245.99,
            "merchant_category": "Online Retail"
        },
        {
            "case_id": "CASE-002",
            "intent_code": "INT-02",
            "intent_name": "Item Not Received",
            "case_description": "I ordered a laptop on February 15th. Tracking shows delivered on Feb 20th but I never received it. I contacted the merchant but no response.",
            "transaction_amount": 899.00,
            "merchant_category": "Electronics"
        },
        {
            "case_id": "CASE-003",
            "intent_code": "INT-04",
            "intent_name": "Canceled Recurring Transaction",
            "case_description": "I canceled my gym membership on January 15th and have the cancellation email. But they charged me again on February 1st for $49.99.",
            "transaction_amount": 49.99,
            "merchant_category": "Fitness"
        }
    ]
    
    for test_case in test_cases:
        result = retriever.retrieve_policies(**test_case)
        
        print("\n" + "=" * 80)
        print(f"CASE: {result['case_id']}")
        print("=" * 80)
        
        print(f"\n📋 APPLICABLE POLICIES ({len(result['applicable_policies'])}):")
        for policy in result["applicable_policies"]:
            print(f"\n  • {policy['policy_id']}: {policy.get('policy_section', 'N/A')}")
            print(f"    Relevance: {policy['relevance_score']:.2f}")
            print(f"    Guidance: {policy['guidance']}")
        
        print(f"\n💡 COMBINED GUIDANCE:")
        print(f"  {result['combined_guidance']}")
        
        print(f"\n🎯 RECOMMENDATION: {result['recommended_action'].upper()}")
        print(f"   Confidence: {result['confidence']:.2f}")
        
        if result.get("missing_information"):
            print(f"\n❓ MISSING INFO:")
            for info in result["missing_information"]:
                print(f"  • {info}")
        
        print(f"\n📊 METADATA:")
        print(f"  Retrieved: {result['num_policies_retrieved']} chunks")
        print(f"  Used: {result['num_policies_used']} policies")
        print(f"  Method: {result['retrieval_method']}")
        
        if result.get("validation_warnings"):
            print(f"\n⚠️  WARNINGS:")
            for warning in result["validation_warnings"]:
                print(f"  • {warning}")
    
    print("\n" + "=" * 80)
