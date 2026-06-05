# dashboard/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from prediction.models import Prediction


@login_required(login_url="/login/")
def dashboard(request):

    predictions = Prediction.objects.filter(
        user=request.user
    ).order_by("-created_at")

    
    total_predictions = Prediction.objects.count()

    recent_predictions = Prediction.objects.order_by(
    "-id"
)[:5]

    context = {

        "username": request.user.username,

        "total_predictions": total_predictions,

        "reports_generated": total_predictions,

        "recent_predictions": recent_predictions,
        "total_predictions": total_predictions,
        "recent_predictions": recent_predictions


    }

    return render(
        request,
        "dashboard.html",
        context
    )