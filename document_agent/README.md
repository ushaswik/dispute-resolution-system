# Document Agent - Multi-Format Processor

Extracts structured information from dispute-related documents using intelligent routing.

## Supported Formats

✅ **Text Files** (.txt) — Direct extraction  
✅ **Word Documents** (.docx) — python-docx extraction  
✅ **Excel Spreadsheets** (.xlsx) — openpyxl extraction  
✅ **PDFs** (.pdf) — PyPDF2 → Tesseract OCR → Vision (fallback)  
✅ **Images** (.jpg, .png, .jpeg) — Tesseract OCR → Vision (fallback)

## Processing Strategy
```
Document → File Type Detection
         ↓
    Route to Processor
         ↓
┌────────────────────────────────┐
│ TEXT/DOCX/XLSX → Direct Parse │
│ PDF → Try Text → OCR → Vision │
│ IMAGE → OCR → Vision Fallback │
└────────────────────────────────┘
         ↓
    GPT Interpretation
         ↓
   Structured JSON Output
```

## OCR Confidence Threshold

- **>70%**: Use OCR text with GPT-4o-mini ($0.001/doc)
- **<70%**: Fallback to GPT-4o Vision ($0.02/image)

## Setup

### Install Tesseract OCR

**macOS:**
```bash
brew install tesseract poppler
```

**Windows:**
- Download Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
- Download Poppler: http://blog.alivate.com.au/poppler-windows/

**Linux:**
```bash
sudo apt-get install tesseract-ocr poppler-utils
```

### Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Configure

Create `.env`:
```
OPENAI_API_KEY=sk-proj-your-key-here
```

## Usage

### Create Test Documents
```bash
python create_test_documents.py
```

### Test Processor
```bash
python document_processor.py
```

### Run API Server
```bash
python main.py
```

Server: http://localhost:8081

## API Example
```bash
curl -X POST http://localhost:8081/upload-and-process \
  -F "case_id=CASE-001" \
  -F "file=@receipt.jpg" \
  -F "intent_name=Lost/Stolen Card"
```

## Cost Comparison

| Method | Cost per Document | Use Case |
|--------|------------------|----------|
| Text Parse | $0.0001 | Digital documents |
| OCR + GPT-mini | $0.001 | Clear scans |
| Vision | $0.02 | Poor quality/complex |

## Output Schema
```json
{
  "merchant_name": "Target",
  "transaction_date": "2026-03-07",
  "transaction_amount": 92.45,
  "items_purchased": ["item1", "item2"],
  "payment_method": "Visa x-4567",
  "extraction_method": "ocr|vision|text_parse",
  "confidence": 0.89,
  "ocr_confidence": 88.5
}
```

## Next: Azure Blob Integration

To connect to Azure Blob Storage, add `azure-storage-blob` and update to download from URLs.