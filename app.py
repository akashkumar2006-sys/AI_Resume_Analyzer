from flask import Flask, render_template, request, send_file
import os
import re
import PyPDF2
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from report import create_report

app = Flask(__name__)


UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER



# Load trained model

model = joblib.load("model/resume_model.pkl")



# Skills database

SKILLS = [
    "Python","C","C++","Java","JavaScript","HTML","CSS","SQL",
    "Machine Learning","Artificial Intelligence","Deep Learning",
    "NLP","Generative AI","Prompt Engineering",
    "TensorFlow","PyTorch","Scikit-learn","Pandas","NumPy",
    "Flask","Django","React",
    "Git","GitHub","Docker","AWS",
    "Excel","Power BI","REST API","OpenCV",
    "Data Structures","Algorithms"
]



def extract_skills(text):

    detected = []

    text = text.lower()


    skill_variations = {

    "Python": ["python"],
    "C": [" c ", " c language"],
    "C++": ["c++", "cpp"],
    "Java": ["java"],
    "JavaScript": ["javascript", "js"],
    "HTML": ["html"],
    "CSS": ["css"],
    "SQL": ["sql", "mysql", "postgresql"],

    "Machine Learning": ["machine learning", "ml"],
    "Artificial Intelligence": ["artificial intelligence", "ai"],
    "Deep Learning": ["deep learning", "dl"],
    "NLP": ["nlp", "natural language processing"],
    "Generative AI": ["generative ai", "gen ai"],
    "Prompt Engineering": ["prompt engineering"],

    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "Scikit-learn": ["scikit", "sklearn"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],

    "Flask": ["flask"],
    "Django": ["django"],
    "React": ["react", "reactjs", "react.js"],

    "Git": ["git"],
    "GitHub": ["github"],
    "Docker": ["docker"],
    "AWS": ["aws", "amazon web services"],

    "Excel": ["excel"],
    "Power BI": ["power bi"],
    "REST API": ["rest api"],
    "OpenCV": ["opencv"],

    "Data Structures": ["data structures", "dsa"],
    "Algorithms": ["algorithms", "algorithm"]
}


    for skill, keywords in skill_variations.items():

        for keyword in keywords:

            if keyword in text:

                detected.append(skill)
                break


    return detected



def calculate_score(text, skills):

    score = 0
    text_lower = text.lower()

    # Contact Information
    if re.search(r'[\w\.-]+@[\w\.-]+', text):
        score += 10

    if re.search(r'\b\d{10}\b', text):
        score += 10

    # Education
    if "education" in text_lower:
        score += 10

    # Experience
    if "experience" in text_lower or "internship" in text_lower:
        score += 15

    # Projects
    if "project" in text_lower:
        score += 15

    # Certifications
    if "certification" in text_lower or "certificate" in text_lower:
        score += 10

    # Skills
    score += min(len(skills) * 2, 20)

    # Resume Length
    words = len(text.split())

    if words >= 300:
        score += 10
    elif words >= 200:
        score += 7
    elif words >= 100:
        score += 5

    return min(score, 100)

def calculate_ats_score(text, skills, prediction):

    score = 0
    text_lower = text.lower()

    # Contact Information
    if re.search(r'[\w\.-]+@[\w\.-]+', text):
        score += 10

    if re.search(r'\b\d{10}\b', text):
        score += 10

    # Standard Resume Sections
    sections = [
        "summary",
        "education",
        "skills",
        "experience",
        "project",
        "certification"
    ]

    for section in sections:
        if section in text_lower:
            score += 8

    # Technical Skills
    score += min(len(skills) * 2, 20)

    # Resume Length
    words = len(text.split())

    if 250 <= words <= 800:
        score += 10

    # Predicted Career Keywords
    if prediction.lower() in text_lower:
        score += 10

    return min(score, 100)

def generate_suggestions(skills, prediction):

    suggestions = []

    recommendations = {
        "AI Engineer": [
            "Deep Learning",
            "TensorFlow",
            "PyTorch",
            "Docker"
        ],
        "ML Engineer": [
            "Scikit-learn",
            "TensorFlow",
            "SQL",
            "Statistics"
        ],
        "Data Analyst": [
            "SQL",
            "Excel",
            "Power BI",
            "Python"
        ],
        "Frontend Developer": [
            "HTML",
            "CSS",
            "JavaScript",
            "React"
        ],
        "Software Engineer": [
            "Data Structures",
            "Algorithms",
            "Git",
            "Docker"
        ]
    }

    required = recommendations.get(prediction, [])

    missing = []

    for skill in required:
        if skill.lower() not in [s.lower() for s in skills]:
            missing.append(skill)

    if missing:
        suggestions.append(
            "Learn these important skills: " + ", ".join(missing)
        )

    if len(skills) < 8:
        suggestions.append(
            "Add more technical skills to strengthen your resume."
        )

    suggestions.append(
        "Include 2–3 real-world projects with measurable outcomes."
    )

    suggestions.append(
        "Add GitHub and LinkedIn profile links."
    )

    suggestions.append(
        "Include internships, certifications, and achievements."
    )

    suggestions.append(
        "Keep your resume ATS-friendly using clear section headings."
    )

    return missing, suggestions



def analyze_resume_quality(text, skills):

    strengths = []
    weaknesses = []

    text_lower = text.lower()

    # Contact
    if re.search(r'[\w\.-]+@[\w\.-]+', text):
        strengths.append("Professional email address detected.")
    else:
        weaknesses.append("Add a professional email address.")

    if re.search(r'\b\d{10}\b', text):
        strengths.append("Phone number detected.")
    else:
        weaknesses.append("Add your phone number.")

    # Skills
    if len(skills) >= 8:
        strengths.append("Excellent technical skill coverage.")
    elif len(skills) >= 5:
        strengths.append("Good technical skill coverage.")
    else:
        weaknesses.append("Add more relevant technical skills.")

    # Sections
    sections = {
        "education": "Education section found.",
        "experience": "Experience section found.",
        "project": "Projects section found.",
        "certification": "Certification section found.",
        "summary": "Professional summary included."
    }

    for section, message in sections.items():
        if section in text_lower:
            strengths.append(message)
        else:
            weaknesses.append(f"Add a {section.title()} section.")

    # Resume Length
    words = len(text.split())

    if words >= 250:
        strengths.append("Resume has a good overall length.")
    else:
        weaknesses.append("Expand your resume with more achievements and projects.")

    return strengths, weaknesses


def extract_contact_info(text):

    name = "Not Found"
    email = "Not Found"
    phone = "Not Found"

    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    if email_match:
        email = email_match.group()

    phone_match = re.search(r'\b\d{10}\b', text)
    if phone_match:
        phone = phone_match.group()

    ignored = [
        "contact","profile","summary","objective",
        "skills","education","experience",
        "projects","certification","languages",
        "at college"
    ]

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    for line in lines[:15]:
        if (
            2 <= len(line.split()) <= 4
            and line.replace(" ", "").replace(".", "").isalpha()
            and line.lower() not in ignored
        ):
            name = line.title()
            break

    return email, phone

# Improved NLP Job Matching

def analyze_job_match(resume_text, job_description):

    if not job_description.strip():
        return 0, [], []

    vectorizer = TfidfVectorizer(stop_words="english")

    vectors = vectorizer.fit_transform([resume_text, job_description])

    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

    match_score = round(similarity * 100)

    resume_words = set(re.findall(r'\b[a-zA-Z][a-zA-Z+#.]*\b', resume_text.lower()))
    job_words = set(re.findall(r'\b[a-zA-Z][a-zA-Z+#.]*\b', job_description.lower()))

    stop_words = {
        "the","and","for","with","from","into","your","our","their",
        "will","have","has","had","this","that","these","those",
        "you","are","who","all","any","can","should","must",
        "using","ability","skills","skill","knowledge","good",
        "work","working","candidate","experience","required"
    }

    resume_words -= stop_words
    job_words -= stop_words

    matched = sorted(list(resume_words & job_words))
    missing = sorted(list(job_words - resume_words))

    return (
        min(match_score, 100),
        matched[:20],
        missing[:20]
    )

def validate_resume(text):

    invalid_keywords = [
        "offer letter",
        "internship offer",
        "congratulations",
        "selected for internship",
        "joining letter",
        "appointment letter"
    ]

    text = text.lower()

    for keyword in invalid_keywords:
        if keyword in text:
            return False

    return True


def extract_text(pdf_path):

    text = ""


    with open(pdf_path, "rb") as file:

        reader = PyPDF2.PdfReader(file)


        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:

                text += page_text



    return text

def get_score_color(score):
    if score >= 80:
        return "green"
    elif score >= 60:
        return "yellow"
    else:
        return "red"


@app.route("/")
def home():

    return render_template("index.html")




@app.route("/analyze", methods=["POST"])
def analyze():


    resume = request.files["resume"]


    job_description = request.form.get(

        "job_description",

        ""

    )



    file_path = os.path.join(

        app.config["UPLOAD_FOLDER"],

        resume.filename

    )


    resume.save(file_path)



    resume_text = extract_text(file_path)

    if not validate_resume(resume_text):

        return render_template(
            "index.html",
            error="This document does not appear to be a resume. Please upload your CV."
    )

    prediction = model.predict(

        [resume_text]

    )[0]



    skills = extract_skills(resume_text)



    score = calculate_score(

        resume_text,

        skills

    )



    ats_score = calculate_ats_score(

        resume_text,

        skills,

        prediction

    )



    missing_skills, suggestions = generate_suggestions(

        skills,

        prediction

    )



    strengths, weaknesses = analyze_resume_quality(

        resume_text,

        skills

    )



    name, email, phone = extract_contact_info(

        resume_text

    )



    job_match, matched_keywords, missing_keywords = analyze_job_match(

        resume_text,

        job_description

    )


    resume_color = get_score_color(score)
    ats_color = get_score_color(ats_score)
    job_color = get_score_color(job_match)


    return render_template(

        "result.html",

        prediction=prediction,

        skills=skills,

        score=score,

        ats_score=ats_score,

        job_match=job_match,

        matched_keywords=matched_keywords,

        missing_keywords=missing_keywords,

        missing_skills=missing_skills,

        suggestions=suggestions,

        strengths=strengths,

        weaknesses=weaknesses,

        name=name,

        email=email,

        phone=phone,

        resume_text=resume_text,
        
        resume_color=resume_color,
        
        ats_color=ats_color,
        
        job_color=job_color,

    )
    
@app.route("/download_report")
def download_report():

    data = {

        "name": request.args.get("name"),

        "email": request.args.get("email"),

        "phone": request.args.get("phone"),

        "prediction": request.args.get("prediction"),

        "score": request.args.get("score"),

        "ats_score": request.args.get("ats_score"),

        "job_match": request.args.get("job_match"),

        "skills": request.args.get("skills", "").split(","),

        "strengths": request.args.get("strengths", "").split(","),

        "weaknesses": request.args.get("weaknesses", "").split(","),

        "suggestions": request.args.get("suggestions", "").split(",")

    }


    filename = "AI_Resume_Analysis_Report.pdf"


    create_report(
        data,
        filename
    )


    return send_file(
        filename,
        as_attachment=True
    )



if __name__ == "__main__":

    app.run(

        debug=True,

        host="0.0.0.0",

        port=5000

    )
