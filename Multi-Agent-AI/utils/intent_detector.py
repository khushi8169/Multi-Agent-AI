import openai
import os
from dotenv import load_dotenv


load_dotenv()

client = openai.OpenAI(api_key = os.getenv("OPENAI_API_KEY"))  # or pass your key directly

def detect_intent_openai(text):
    prompt = f""" You are an intelligent assistant. Read the following text and identify the **intent** behind it.
                Return only one word from this list: ["invoice", "rfq", "complaint", "other"].
                Text: \"{text}\"
                Intent:
            """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that classifies document intent."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        return response.choices[0].message.content.strip().lower()
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    sample_text = """Dear supplier, please send us a quotation for the attached items including delivery time and warranty information.
                    """
    print("Detected Intent:", detect_intent_openai(sample_text))
