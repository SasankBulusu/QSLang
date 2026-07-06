import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def get_ai_explanation(payload: list, error: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "AI Tutor unavailable: GEMINI_API_KEY not found in .env file."

    client = genai.Client(api_key=api_key)

    if error:
        prompt = f"""
You are an expert quantum computing teaching assistant.
A student got this error in their quantum circuit program:

ERROR: {error}

In exactly 3 bullet points:
- Explain simply what this error means
- Explain WHY this is a rule in quantum computing
- Give a corrected example code snippet

Keep your response clear, encouraging, and beginner-friendly.
"""
    else:
        circuit_description = ", ".join(
            [f"{inst['gate']} gate on qubit {inst['target']}" for inst in payload]
        )
        prompt = f"""
You are an expert quantum computing teaching assistant.
A student successfully compiled this quantum circuit:

Circuit operations: {circuit_description}

In exactly 3 bullet points:
- Explain what each gate does physically (in simple terms)
- Explain what quantum phenomenon this circuit demonstrates
- Suggest one thing the student could add or change to explore further

Keep your response clear, enthusiastic, and educational.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"AI Tutor is currently unavailable: {str(e)}"
    
if __name__ == "__main__":
    test_payload = [{"gate": "H", "target": 0}, {"gate": "CNOT", "target": 1}]
    explanation = get_ai_explanation(test_payload, "")
    print(explanation)