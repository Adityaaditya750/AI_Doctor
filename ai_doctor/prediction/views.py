from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Prediction
from .symptoms import all_symptoms
import joblib
from accounts.models import UserProfile
import google.generativeai as genai
from django.http import HttpResponse
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

genai.configure(
    api_key="AIzaSyCNLrBtIvtq54N8NUnnK0ewF2JxnIOWlR0"
)

gemini_model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# model = joblib.load(
#     "prediction/disease_model.pkl"
# )

model = joblib.load("prediction/disease_model.pkl")


@login_required(login_url="/login/")
def predict_disease(request):

    prediction = None
    confidence = None
    ai_report = None
    prediction_id = None

    if request.method == "POST":

        user_text = request.POST.get(
            "symptoms",
            ""
        ).lower()

        vector = []

        for symptom in all_symptoms:

            symptom_name = symptom.replace(
                "_",
                " "
            )

            if symptom_name in user_text:
                vector.append(1)
            else:
                vector.append(0)

        prediction = model.predict(
            [vector]
        )[0]

        doctor_mapping = {
            "Heart Attack": "Cardiologist",
            "Acne": "Dermatologist",
            "Arthritis": "Orthopedic",
            "Diabetes": "Endocrinologist",
            "Common Cold": "General Physician",
            "Dengue": "General Physician",
            "Fungal Infection": "Dermatologist",
            "Hypertension": "Cardiologist",
            "Migraine": "Neurologist",
            "Pneumonia": "Pulmonologist"
        }

        recommended_doctor = doctor_mapping.get(
            prediction,
            "General Physician"
        )

        confidence = 95

        prompt = f"""
Disease: {prediction}

Generate a professional medical report.

Format:

Disease:
Description:
Possible Causes:
Precautions:
Recommended Medicines:
Diet Advice:
Lifestyle Advice:
When To Visit Doctor:

Keep the answer concise and professional.
"""

        response = gemini_model.generate_content(
            prompt
        )

        ai_report = response.text

        prediction_obj = Prediction.objects.create(
            user=request.user,
            disease=prediction,
            confidence=confidence,
            symptoms=user_text,
            report=ai_report
        )
        prediction_id = prediction_obj.id

    return render(
        request,
        "predict.html",
        {
            "prediction": prediction,
            "confidence": confidence,
            "ai_report": ai_report,
            "prediction_id": prediction_id
        }
    )

def download_report(request, prediction_id):

    prediction = Prediction.objects.get(
        id=prediction_id
    )

    profile, created = UserProfile.objects.get_or_create(
    user=request.user,
    defaults={
        "full_name": request.user.username,
        "age": 0,
        "gender": "Not Specified"
    }
)

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        'attachment; filename="AI_Doctor_Report.pdf"'
    )

    doc = SimpleDocTemplate(response)

    styles = getSampleStyleSheet()

    story = []

    # Header
    story.append(
        Paragraph(
            "AI DOCTOR MEDICAL REPORT",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            "AI Powered Healthcare Analysis",
            styles["Italic"]
        )
    )

    story.append(
        Spacer(1, 20)
    )

    # Patient Information
    story.append(
        Paragraph(
            "<b>PATIENT INFORMATION</b>",
            styles["Heading2"]
        )
    )

    patient_data = [
        ["Full Name", profile.full_name],
        ["Age", str(profile.age)],
        ["Gender", profile.gender],
        ["Username", request.user.username],
        ["Date", prediction.created_at.strftime("%d-%m-%Y %H:%M")]
    ]

    patient_table = Table(
        patient_data,
        colWidths=[120, 300]
    )

    patient_table.setStyle(
        TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold')
        ])
    )

    story.append(patient_table)

    story.append(
        Spacer(1, 20)
    )

    # Disease Summary
    story.append(
        Paragraph(
            "<b>DISEASE SUMMARY</b>",
            styles["Heading2"]
        )
    )

    disease_data = [
        ["Predicted Disease", prediction.disease],
        ["Confidence Score", f"{prediction.confidence}%"]
    ]

    disease_table = Table(
        disease_data,
        colWidths=[180, 240]
    )

    disease_table.setStyle(
        TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgreen),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold')
        ])
    )

    story.append(disease_table)

    story.append(
        Spacer(1, 20)
    )

    # Symptoms
    story.append(
        Paragraph(
            "<b>SYMPTOMS PROVIDED</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            prediction.symptoms,
            styles["BodyText"]
        )
    )

    story.append(
        Spacer(1, 20)
    )

    # AI Analysis
    story.append(
        Paragraph(
            "<b>AI MEDICAL ANALYSIS</b>",
            styles["Heading2"]
        )
    )

    report_text = prediction.report

    if not report_text:
        report_text = "No AI Medical Analysis Available."

    story.append(
        Paragraph(
            report_text.replace("\n", "<br/>"),
            styles["BodyText"]
        )
    )

    story.append(
        Spacer(1, 20)
    )

    # Health Advice
    story.append(
        Paragraph(
            "<b>GENERAL HEALTH ADVICE</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            """
            • Follow prescribed medication.<br/>
            • Drink adequate water.<br/>
            • Maintain a healthy diet.<br/>
            • Take proper rest and sleep.<br/>
            • Consult a doctor if symptoms worsen.
            """,
            styles["BodyText"]
        )
    )

    story.append(
        Spacer(1, 20)
    )

    # Signature
    story.append(
        Paragraph(
            "____________________________",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            "AI Doctor Digital Signature",
            styles["Italic"]
        )
    )

    story.append(
        Spacer(1, 20)
    )

    # Disclaimer
    story.append(
        Paragraph(
            "<b>DISCLAIMER</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            "This report is generated using Artificial Intelligence and is intended for educational purposes only. Please consult a qualified healthcare professional before taking any medication.",
            styles["BodyText"]
        )
    )

    doc.build(story)

    return response