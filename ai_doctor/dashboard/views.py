from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from prediction.models import Prediction
from chatbot.models import ChatHistory
from accounts.models import UserProfile


@login_required(login_url="/login/")
def dashboard(request):

    profile = UserProfile.objects.get(
        user=request.user
    )

    user_predictions = Prediction.objects.filter(
        user=request.user
    )

    total_predictions = user_predictions.count()

    recent_predictions = user_predictions.order_by(
        "-created_at"
    )[:5]

    total_chats = ChatHistory.objects.filter(
        user=request.user
    ).count()

    context = {

        "username": request.user.username,

        "total_predictions": total_predictions,

        "reports_generated": profile.reports_downloaded,

        "recent_predictions": recent_predictions,

        "total_chats": total_chats,

    }

    return render(
        request,
        "dashboard.html",
        context
    )