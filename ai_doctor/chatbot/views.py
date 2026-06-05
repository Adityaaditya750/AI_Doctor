from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ChatHistory
import google.generativeai as genai

genai.configure(
    api_key="AIzaSyCNLrBtIvtq54N8NUnnK0ewF2JxnIOWlR0"
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

Provide safe healthcare guidance.
Do not prescribe dangerous medicines.
Recommend consulting a doctor when needed.
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