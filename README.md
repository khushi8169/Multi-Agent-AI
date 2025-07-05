# Multi‑Agent Document Processing System

&#x20;

A lightweight AI‑driven pipeline that **accepts raw PDF, JSON, or e‑mail files, classifies both the file format and business intent (Invoice, RFQ, Complaint, etc.), routes the input to a specialized agent**, and stores every step in a shared SQLite memory for full traceability.

---

## ✨ Key Features

| Feature                           | Description                                                               |
| --------------------------------- | ------------------------------------------------------------------------- |
| **Classifier Agent**              | Detects file **format** & **intent**, then routes to the correct agent.   |
| **JSON Agent**                    | Maps JSON payloads to target schema, flags missing fields / anomalies.    |
| **Email Agent**                   | Extracts sender, urgency, & intent, formats output for CRM ingestion.     |
| **PDF Agent**                     | (Basic) extracts text with *PyMuPDF*, detects invoice fields.             |
| **Shared Memory (SQLite)**        | Persists source, type, intent, extracted fields, timestamps & thread‑IDs. |
| **Pluggable LLM Intent Detector** | Works with OpenAI GPT‑3.5/4 (default) or Google Gemini.                   |

---

## 🗃️ Folder Structure

```text
multi_agent_ai/
├── main.py                # unified entry‑point
├── classifier_agent.py    # format + intent classifier
├── email_agent.py         # e‑mail extractor
├── json_agent.py          # JSON normaliser
├── pdf_agent.py           # PDF extractor
├── shared_memory.py       # lightweight SQLite wrapper
├── utils/
│   ├── intent_detector.py # OpenAI / Gemini intent helper
│   └── file_parser.py     # (optional) extra helpers
├── data/                  # sample inputs (PDF / JSON / e‑mail)
├── output_logs/           # auto‑generated logs
├── requirements.txt       # Python deps
└── README.md              # you are here
```

---

## 🚀 Quick‑start

### 1. Clone & create a virtualenv  *(recommended)*

```bash
git clone https://github.com/khushi8169/multi_agent_ai.git
cd multi_agent_ai
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note**
> For PDF parsing you need **PyMuPDF** which currently supports Python ≤3.12.
> If you hit a build error on PyMuPDF, switch to Python 3.11.

### 3. Environment variables

```bash
# OpenAI (default) – required for intent detection
export OPENAI_API_KEY="sk‑..."

# Optional: Google Gemini
# export GOOGLE_API_KEY="..."
```

### 4. Run the pipeline

```bash
# Email example
python main.py data/sample_email.txt

# JSON example (RFQ)
python main.py data/sample_rfq.json

# PDF example (Invoice)
python main.py data/sample_invoice.pdf
```

Inspect the resulting rows in SQLite:

```bash
python - << 'PY'
from shared_memory import fetch_all_logs
for row in fetch_all_logs():
    print(row)
PY
```

---

## 🛠️ Configuration & Extensibility

| Setting             | How to change                                                          |
| ------------------- | ---------------------------------------------------------------------- |
| **LLM provider**    | Swap `detect_intent_openai` with Gemini in `utils/intent_detector.py`. |
| **Schema rules**    | Edit `SCHEMA_MAP` in `json_agent.py`.                                  |
| **PDF field regex** | Adjust regexes in `pdf_agent.py::extract_invoice_fields`.              |
| **Storage backend** | Replace `sqlite3` calls in `shared_memory.py` with Redis / PostgreSQL. |


---

## 📦 Deployment (optional FastAPI)

If you wish to expose the pipeline as an HTTP service:

```bash
pip install fastapi uvicorn
uvicorn api:app --reload  # example FastAPI file `api.py` not included
```

---

## 📝 Contributing

1. Fork the repo
2. Create a branch: `git checkout -b feature/awesome`
3. Commit: `git commit -m "Add awesome feature"`
4. Push: `git push origin feature/awesome`
5. Open a pull request

---

## 🗄️ Git Commands to Publish Your Project

```bash
# inside project root
git init

git add .
git commit -m "Initial multi‑agent system"

# Replace with your remote repo URL
git remote add origin https://github.com/khushi8169/multi_agent_ai.git
git branch -M main
git push -u origin main
```

---

## 📜 License

MIT © 2025 KHUSHI SINGH. See `LICENSE` for details.
