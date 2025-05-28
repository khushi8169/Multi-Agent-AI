from classifier_agent import classify_input
from email_agent import process_email
from json_agent import process_json_file
from pdf_agent import process_pdf_file

def main(filepath):
    print(f"Processing file: {filepath}\n")
    file_type, intent, thread_id, content = classify_input(filepath)

    if file_type == "Email":
        result = process_email(content, source_file=filepath, thread_id=thread_id)
    elif file_type == "JSON":
        result = process_json_file(filepath)
    elif file_type == "PDF":
        result = process_pdf_file(filepath)
    else:
        print("[✗] Unknown file type.")
        result = None

    print("\nResult:")
    print(result)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py <filepath>")
        sys.exit(1)
    main(sys.argv[1])
