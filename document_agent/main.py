"""
Document Agent - REST API Server
Processes documents and extracts structured information
Supports: TXT, DOCX, XLSX, PDF, JPG, PNG
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from pydantic import BaseModel
from typing import Optional
from doc_processor import DocumentProcessor
import uvicorn
import os
import shutil

app = FastAPI(
    title="Document Agent API",
    description="Extracts information from dispute-related documents (multi-format support)",
    version="2.0.0"
)

processor = DocumentProcessor()

# Ensure upload directory exists
UPLOAD_DIR = "uploaded_documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ==================== REQUEST/RESPONSE MODELS ====================

class ProcessRequest(BaseModel):
    """Request model for processing a file already on server"""
    case_id: str
    document_path: str
    intent_name: Optional[str] = None
    disputed_amount: Optional[float] = None
    transaction_date: Optional[str] = None


class ProcessResponse(BaseModel):
    """Response model for document processing"""
    case_id: str
    
    # Core transaction info
    merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    transaction_amount: Optional[float] = None
    transaction_currency: Optional[str] = None
    
    # Details
    items_purchased: Optional[list] = None
    payment_method: Optional[str] = None
    card_last_four: Optional[str] = None
    order_number: Optional[str] = None
    
    # Document metadata
    document_type: Optional[str] = None
    extraction_method: Optional[str] = None
    
    # Dispute analysis
    key_evidence: Optional[list] = None
    supports_dispute: Optional[bool] = None
    dispute_relevance: Optional[str] = None
    
    # Quality metrics
    confidence: Optional[float] = None
    ocr_confidence: Optional[float] = None
    
    # File info
    file_name: Optional[str] = None
    file_type: Optional[str] = None
    processing_timestamp: Optional[str] = None


# ==================== ENDPOINTS ====================

@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "service": "Document Agent",
        "status": "healthy",
        "version": "2.0.0",
        "supported_formats": [
            "txt", "docx", "xlsx", "pdf", 
            "jpg", "jpeg", "png", "gif", "bmp"
        ],
        "features": [
            "Tesseract OCR",
            "GPT-4o Vision fallback",
            "Multi-format support",
            "Intelligent routing"
        ]
    }


@app.get("/health")
def health_check():
    """Kubernetes health check"""
    return {"status": "healthy"}


@app.post("/process", response_model=ProcessResponse)
def process_document(request: ProcessRequest):
    """
    Process a document that's already saved on the server
    
    Args:
        request: ProcessRequest with document path and context
        
    Returns:
        Extracted information as ProcessResponse
    """
    try:
        # Build dispute context
        context = {
            "intent_name": request.intent_name,
            "disputed_amount": request.disputed_amount,
            "transaction_date": request.transaction_date
        }
        
        # Process document
        result = processor.process_document(request.document_path, context)
        
        # Add case_id
        result["case_id"] = request.case_id
        
        return result
        
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=f"Document not found: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {str(e)}"
        )


@app.post("/upload-and-process", response_model=ProcessResponse)
async def upload_and_process(
    case_id: str = Form(...),
    file: UploadFile = File(...),
    intent_name: Optional[str] = Form(None),
    disputed_amount: Optional[float] = Form(None),
    transaction_date: Optional[str] = Form(None)
):
    """
    Upload a document and process it in one step
    
    Accepts file upload via multipart/form-data
    
    Supported formats:
    - Images: JPG, JPEG, PNG, GIF, BMP
    - Documents: PDF, TXT, DOCX, XLSX
    
    Example using curl:
```bash
    curl -X POST http://localhost:8081/upload-and-process \
      -F "case_id=CASE-001" \
      -F "file=@receipt.jpg" \
      -F "intent_name=Lost/Stolen Card" \
      -F "disputed_amount=26.37"
```
    """
    
    file_path = None
    
    try:
        # Validate file extension
        file_extension = os.path.splitext(file.filename)[1].lower()
        supported_extensions = [
            '.txt', '.pdf', '.docx', '.xlsx',
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'
        ]
        
        if file_extension not in supported_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_extension}. Supported: {', '.join(supported_extensions)}"
            )
        
        # Save uploaded file
        file_path = os.path.join(UPLOAD_DIR, f"{case_id}_{file.filename}")
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        print(f"📤 Uploaded: {file.filename} → {file_path}")
        
        # Build dispute context
        context = {
            "intent_name": intent_name,
            "disputed_amount": disputed_amount,
            "transaction_date": transaction_date
        }
        
        # Process document
        result = processor.process_document(file_path, context)
        
        # Add case_id
        result["case_id"] = case_id
        
        print(f"✅ Processed successfully: {result.get('extraction_method')}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Upload and process failed: {str(e)}"
        )
    finally:
        # Clean up uploaded file after processing
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"🗑️  Cleaned up: {file_path}")
            except Exception as e:
                print(f"⚠️  Failed to clean up {file_path}: {e}")


@app.get("/supported-formats")
def get_supported_formats():
    """
    Get list of supported file formats and processing methods
    """
    return {
        "text_files": {
            "extensions": [".txt"],
            "method": "Direct text extraction",
            "cost_per_doc": "$0.0001"
        },
        "word_documents": {
            "extensions": [".docx"],
            "method": "python-docx extraction",
            "cost_per_doc": "$0.0001"
        },
        "excel_spreadsheets": {
            "extensions": [".xlsx"],
            "method": "openpyxl extraction",
            "cost_per_doc": "$0.0001"
        },
        "pdf_files": {
            "extensions": [".pdf"],
            "method": "Text extraction → Tesseract OCR → Vision (fallback)",
            "cost_per_doc": "$0.001 - $0.02 (depending on quality)"
        },
        "images": {
            "extensions": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
            "method": "Tesseract OCR → Vision (fallback)",
            "cost_per_doc": "$0.001 - $0.02 (depending on quality)"
        },
        "ocr_confidence_threshold": 70.0,
        "fallback_strategy": "If OCR confidence < 70%, fallback to GPT-4o Vision"
    }


@app.get("/stats")
def get_stats():
    """
    Get processing statistics (placeholder - would connect to database in production)
    """
    return {
        "total_documents_processed": "N/A",
        "avg_confidence_score": "N/A",
        "most_common_extraction_method": "N/A",
        "note": "Stats would be tracked in production database"
    }


# ==================== RUN SERVER ====================

if __name__ == "__main__":
    print("=" * 80)
    print("🚀 DOCUMENT AGENT API SERVER")
    print("=" * 80)
    print()
    print("Supported formats:")
    print("  ✅ Text files (.txt)")
    print("  ✅ Word documents (.docx)")
    print("  ✅ Excel spreadsheets (.xlsx)")
    print("  ✅ PDF files (.pdf)")
    print("  ✅ Images (.jpg, .png, .jpeg, .gif, .bmp)")
    print()
    print("Processing methods:")
    print("  📝 Text extraction → GPT-4o-mini ($0.0001/doc)")
    print("  🔍 Tesseract OCR → GPT-4o-mini ($0.001/doc)")
    print("  👁️  GPT-4o Vision (fallback) ($0.02/doc)")
    print()
    print("Starting server...")
    print("  Local:   http://localhost:8081")
    print("  Docs:    http://localhost:8081/docs")
    print("  Health:  http://localhost:8081/health")
    print()
    print("=" * 80)
    print()
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8081,
        reload=True  # Auto-reload on code changes
    )