import json
from shared_memory import log_entry
from uuid import uuid4
from classifier_agent import detect_intent

# Define expected fields for different intents
SCHEMA_MAP = {
    "Invoice": ["invoice_id", "amount", "date", "vendor"],
    "RFQ": ["rfq_id", "items", "due_date", "customer"],
    "Complaint": ["complaint_id", "issue", "product", "submitted_by"],
    "Regulation": ["reg_id", "title", "effective_date"]
}

def validate_json(payload, intent):
    required_fields = SCHEMA_MAP.get(intent, [])
    missing = []
    anomalies = []

    for field in required_fields:
        if field not in payload:
            missing.append(field)
        elif not isinstance(payload[field], (str, int, float, list, dict)):
            anomalies.append((field, type(payload[field]).__name__))

    return missing, anomalies

def reformat_json(payload, intent):
    formatted = {key: payload.get(key, "N/A") for key in SCHEMA_MAP.get(intent, [])}
    return formatted

def process_json_file(filepath):
    with open(filepath, 'r') as f:
        content = json.load(f)

    raw_text = json.dumps(content)
    intent = detect_intent(raw_text)

    missing, anomalies = validate_json(content, intent)
    reformatted = reformat_json(content, intent)

    result = {
        "intent": intent,
        "reformatted": reformatted,
        "missing_fields": missing,
        "anomalies": anomalies
    }

    log_entry(
        source=filepath,
        file_type="JSON",
        intent=intent,
        extracted_fields=result,
        thread_id=str(uuid4())
    )

    print(f"[✓] JSON Processed: Intent: {intent}, Missing: {missing}, Anomalies: {anomalies}")
    return result
