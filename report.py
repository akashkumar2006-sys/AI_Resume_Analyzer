from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def create_report(data, filename):

    doc = SimpleDocTemplate(filename)


    styles = getSampleStyleSheet()

    content = []


    text = f"""

AI Resume Analyzer Report


Candidate Name:
{data['name']}


Email:
{data['email']}


Phone:
{data['phone']}


Recommended Career:
{data['prediction']}


Resume Score:
{data['score']}%


ATS Score:
{data['ats_score']}%


Job Match:
{data['job_match']}%


Skills:
{', '.join(data['skills'])}


Strengths:
{', '.join(data['strengths'])}


Weaknesses:
{', '.join(data['weaknesses'])}


Suggestions:
{', '.join(data['suggestions'])}

"""


    content.append(
        Paragraph(
            text.replace("\n","<br/>"),
            styles["Normal"]
        )
    )


    content.append(
        Spacer(1,20)
    )


    doc.build(content)
