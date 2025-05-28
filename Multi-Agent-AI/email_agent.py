import re
from shared_memory import log_entry
from uuid import uuid4
from classifier_agent import detect_intent

def extract_sender(text):
    match = re.search(r"From:\s*(.*)", text)
    if match:
        return match.group(1).strip()
    match = re.search(r"([\w\.-]+@[\w\.-]+)", text)
    return match.group(1) if match else "Unknown"

def extract_urgency(text):
    urgency_keywords = ["urgent", "asap", "immediately", "priority", "high importance"]
    text_lower = text.lower()
    for word in urgency_keywords:
        if word in text_lower:
            return "High"
    return "Normal"

def process_email(content, source_file=None, thread_id=None):
    sender = extract_sender(content)
    urgency = extract_urgency(content)
    intent = detect_intent(content)  # re-confirm or re-assign intent

    result = {
        "sender": sender,
        "urgency": urgency,
        "intent": intent,
        "preview": content[:100]
    }

    # Log into shared memory
    log_entry(
        source=source_file or "email_direct_input",
        file_type="Email",
        intent=intent,
        extracted_fields=result,
        thread_id=thread_id or str(uuid4())
    )

    print(f"[✓] Email Processed: Sender: {sender}, Urgency: {urgency}, Intent: {intent}")
    return result
