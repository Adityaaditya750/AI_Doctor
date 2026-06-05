from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph
)

def create_report(
    filename,
    disease,
    confidence
):

    pdf = SimpleDocTemplate(
        filename
    )

    content = [

        Paragraph(
            "AI Doctor Report"
        ),

        Paragraph(
            f"Disease: {disease}"
        ),

        Paragraph(
            f"Confidence: {confidence}%"
        ),

    ]

    pdf.build(content)