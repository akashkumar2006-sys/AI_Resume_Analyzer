from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter


def create_report(data, filename):

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter
    )


    styles = getSampleStyleSheet()


    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontSize=20,
        spaceAfter=20
    )


    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading2"],
        spaceBefore=15,
        spaceAfter=10
    )


    normal_style = styles["Normal"]


    content = []


    # Title

    content.append(
        Paragraph(
            "AI Resume Analyzer Report",
            title_style
        )
    )


    content.append(
        Spacer(1,20)
    )


    # Candidate Details

    content.append(
        Paragraph(
            "Candidate Information",
            heading_style
        )
    )


    candidate_data = [

        ["Name", data["name"]],

        ["Email", data["email"]],

        ["Phone", data["phone"]]

    ]


    table = Table(candidate_data)


    table.setStyle(
        TableStyle([
            ("GRID",(0,0),(-1,-1),0.5,None),
            ("VALIGN",(0,0),(-1,-1),"TOP")
        ])
    )


    content.append(table)


    # Analysis

    content.append(
        Paragraph(
            "AI Analysis",
            heading_style
        )
    )


    analysis = [

        ["Career Prediction", data["prediction"]],

        ["Resume Score", str(data["score"]) + "%"],

        ["ATS Score", str(data["ats_score"]) + "%"],

        ["Job Match", str(data["job_match"]) + "%"]

    ]


    analysis_table = Table(analysis)


    analysis_table.setStyle(
        TableStyle([
            ("GRID",(0,0),(-1,-1),0.5,None)
        ])
    )


    content.append(analysis_table)



    # Skills

    content.append(
        Paragraph(
            "Detected Skills",
            heading_style
        )
    )


    content.append(
        Paragraph(
            ", ".join(data["skills"]),
            normal_style
        )
    )


    # Strengths

    content.append(
        Paragraph(
            "Strengths",
            heading_style
        )
    )


    for item in data["strengths"]:

        content.append(
            Paragraph(
                "• " + item,
                normal_style
            )
        )


    # Weaknesses

    content.append(
        Paragraph(
            "Weaknesses",
            heading_style
        )
    )


    for item in data["weaknesses"]:

        content.append(
            Paragraph(
                "• " + item,
                normal_style
            )
        )


    # Suggestions

    content.append(
        Paragraph(
            "AI Suggestions",
            heading_style
        )
    )


    for item in data["suggestions"]:

        content.append(
            Paragraph(
                "• " + item,
                normal_style
            )
        )


    doc.build(content)
