import fitz  # PyMuPDF
from shared_memory import log_entry
from uuid import uuid4
from classifier_agent import detect_intent

def extract_text_from_pdf(filepath):
    doc = fitz.open(filepath)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_invoice_fields(text):
    # Basic example: extract invoice number and date using regex
    import re
    invoice_no = None
    date = None

    inv_match = re.search(r"Invoice\s*#?:?\s*(\S+)", text, re.IGNORECASE)
    if inv_match:
        invoice_no = inv_match.group(1)

    date_match = re.search(r"Date\s*:? (\d{4}-\d{2}-\d{2})", text)
    if date_match:
        date = date_match.group(1)

    return {
        "invoice_number": invoice_no or "Unknown",
        "invoice_date": date or "Unknown"
    }

def process_pdf_file(filepath):
    text = extract_text_from_pdf(filepath)
    intent = detect_intent(text)
    extracted_fields = {}

    if intent.lower() == "invoice":
        extracted_fields = extract_invoice_fields(text)

    result = {
        "intent": intent,
        "extracted_fields": extracted_fields,
        "preview": text[:200]
    }

    log_entry(
        source=filepath,
        file_type="PDF",
        intent=intent,
        extracted_fields=result,
        thread_id=str(uuid4())
    )

    print(f"[✓] PDF Processed: Intent: {intent}, Fields: {extracted_fields}")
    return result
