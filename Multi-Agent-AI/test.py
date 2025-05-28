# from classifier_agent import classify_input
# from email_agent import process_email

# # First classify input
# file_type, intent, thread_id, content = classify_input("data/sample_email.txt")

# # Now process email
# if file_type == "Email":
#     process_email(content, source_file="data/sample_email.txt", thread_id=thread_id)
from json_agent import process_json_file

process_json_file("data/sample_rfq.json")
