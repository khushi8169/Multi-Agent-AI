import os
import json
import mimetypes
from shared_memory import log_entry
from uuid import uuid4

# Utility to read file content
def read_file(filepath):
    if filepath.endswith(".json"):
        with open(filepath, 'r') as f:
            return f.read()
    elif filepath.endswith(".pdf"):
        import fitz  # PyMuPDF
        doc = fitz.open(filepath)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    else:  # .txt or email
        with open(filepath, 'r') as f:
            return f.read()

# Detect file format
def detect_format(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".pdf":
        return "PDF"
    elif ext == ".json":
        return "JSON"
    else:
        return "Email"

# Simple intent classifier
def detect_intent(text):
    intent_keywords = {
        "Invoice": ["invoice", "amount due", "billing"],
        "RFQ": ["quote", "quotation", "request for quote", "pricing"],
        "Complaint": ["issue", "problem", "not working", "complaint"],
        "Regulation": ["policy", "compliance", "regulation"],
    }
    text_lower = text.lower()
    for intent, keywords in intent_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                return intent
    return "Unknown"

# Main classifier
def classify_input(filepath):
    file_type = detect_format(filepath)
    content = read_file(filepath)
    intent = detect_intent(content)
    
    thread_id = str(uuid4())
    log_entry(
        source=filepath,
        file_type=file_type,
        intent=intent,
        extracted_fields={"raw_preview": content[:150]},
        thread_id=thread_id
    )
    print(f"[✓] Classified: {file_type} + {intent} → Routed to corresponding agent.")
    return file_type, intent, thread_id, content
