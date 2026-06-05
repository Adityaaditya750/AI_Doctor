from django.urls import path
from .views import *

urlpatterns = [

    path(
        "predict/",
        predict_disease,
        name="predict"
    ),

    path(
        "download-report/<int:prediction_id>/",
        download_report,
        name="download_report"
    ),
]