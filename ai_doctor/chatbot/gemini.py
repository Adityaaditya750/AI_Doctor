import google.generativeai as genai

genai.configure(
    api_key="YOUR_API_KEY"
)

model = genai.GenerativeModel(
    "gemini-1.5-flash"
)

def ask_ai(question):

    response = model.generate_content(
        question
    )

    return response.text