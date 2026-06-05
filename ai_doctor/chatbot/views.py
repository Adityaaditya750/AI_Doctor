from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ChatHistory
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()

import os

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


@login_required
def chatbot_view(request):

    if request.method == "POST":

        user_message = request.POST.get(
            "message",
            ""
        ).strip()

        # Prevent empty messages
        if user_message:

            previous_chats = ChatHistory.objects.filter(
                user=request.user
            ).order_by("-id")[:5]

            history = ""

            for chat in previous_chats:

                history += f"""
User: {chat.message}
Bot: {chat.response}
"""

            prompt = f"""
Previous Conversation:

{history}

Current User Message:

{user_message}

You are an AI Doctor Assistant.

Rules:

1. Give helpful healthcare information.
2. You may suggest common over-the-counter (OTC) medicines when appropriate.
3. For medicines, clearly state they are general suggestions and not a prescription.
4. Include:
   - Possible condition
   - Common medicines
   - Precautions
   - Home remedies
   - When to visit a doctor
5. Never claim to be a real doctor.
6. Never prescribe exact treatment for serious diseases.
7. For fever, cold, headache, cough, acidity, minor pain, etc., provide common OTC medicine examples.
8. End every answer with:
   "Consult a qualified healthcare professional for diagnosis and treatment."

Example:

Condition: Fever

Common OTC Medicines:
• Paracetamol (Acetaminophen)
• Ibuprofen

Precautions:
• Follow package instructions.
• Do not exceed recommended dosage.

Home Care:
• Rest
• Drink plenty of fluids

Consult a qualified healthcare professional for diagnosis and treatment.
"""

            response = model.generate_content(
                prompt
            )

            ChatHistory.objects.create(
                user=request.user,
                message=user_message,
                response=response.text
            )

    chats = ChatHistory.objects.filter(
        user=request.user
    ).order_by("id")

    return render(
        request,
        "chatbot.html",
        {
            "chats": chats
        }
    )