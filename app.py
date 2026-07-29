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

    "Python",
    "Machine Learning",
    "Artificial Intelligence",
    "AI",
    "SQL",
    "Excel",
    "HTML",
    "CSS",
    "JavaScript",
    "Java",
    "C++",
    "Data Structures",
    "Algorithms",
    "TensorFlow",
    "Deep Learning",
    "Flask",
    "React",
    "Power BI",
    "PyTorch",
    "Django",
    "AWS",
    "Docker"

]



def extract_skills(text):

    detected = []

    text = text.lower()


    skill_variations = {

        "Python": [
            "python"
        ],

        "Machine Learning": [
            "machine learning",
            "ml"
        ],

        "Artificial Intelligence": [
            "artificial intelligence",
            "ai"
        ],

        "SQL": [
            "sql",
            "mysql",
            "postgresql"
        ],

        "JavaScript": [
            "javascript",
            "js"
        ],

        "React": [
            "react",
            "react.js",
            "reactjs"
        ],

        "C++": [
            "c++",
            "cpp"
        ],

        "Deep Learning": [
            "deep learning",
            "dl"
        ],

        "NLP": [
            "nlp",
            "natural language processing"
        ],

        "Flask": [
            "flask"
        ],

        "TensorFlow": [
            "tensorflow"
        ],

        "PyTorch": [
            "pytorch"
        ],

        "Docker": [
            "docker"
        ],

        "AWS": [
            "aws",
            "amazon web services"
        ]

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


    score += min(len(skills) * 5, 40)


    if len(text) > 1000:

        score += 20

    elif len(text) > 500:

        score += 10


    sections = [

        "education",
        "project",
        "experience",
        "certification",
        "skills"

    ]


    for section in sections:

        if section in text_lower:

            score += 8


    return min(score, 100)




def calculate_score(text, skills):

    score = 0

    text_lower = text.lower()


    # Contact information

    if re.search(r'[\w\.-]+@[\w\.-]+', text):

        score += 10


    if re.search(r'\b\d{10}\b', text):

        score += 10



    # Technical skills

    score += min(len(skills) * 5, 30)



    # Resume sections

    sections = {

        "education": 10,

        "experience": 10,

        "project": 10,

        "certification": 5,

        "summary": 5

    }


    for section, points in sections.items():

        if section in text_lower:

            score += points



    # Length check

    if len(text) > 500:

        score += 5



    return min(score, 100)


def generate_suggestions(skills, prediction):

    recommended = {

        "AI Engineer": [
            "Deep Learning",
            "TensorFlow",
            "PyTorch",
            "SQL"
        ],

        "ML Engineer": [
            "Deep Learning",
            "TensorFlow",
            "Statistics"
        ],

        "Data Analyst": [
            "SQL",
            "Excel",
            "Power BI"
        ],

        "Frontend Developer": [
            "JavaScript",
            "React",
            "UI Design"
        ],

        "Software Engineer": [
            "Data Structures",
            "Algorithms",
            "System Design"
        ]

    }


    required = recommended.get(prediction, [])


    missing = []


    for skill in required:

        if skill.lower() not in [s.lower() for s in skills]:

            missing.append(skill)



    suggestions = [

        "Add more practical projects",

        "Add certifications and experience"

    ]


    if len(skills) < 5:

        suggestions.append(
            "Add more technical skills"
        )


    if missing:

        suggestions.append(
            "Learn missing skills for better career opportunities"
        )


    return missing, suggestions




def analyze_resume_quality(text, skills):

    strengths = []

    weaknesses = []

    text_lower = text.lower()



    if len(skills) >= 5:

        strengths.append(
            "Strong technical skill coverage"
        )

    else:

        weaknesses.append(
            "Add more technical skills"
        )



    if "project" in text_lower:

        strengths.append(
            "Projects section detected"
        )

    else:

        weaknesses.append(
            "Add projects section"
        )



    if "experience" in text_lower or "internship" in text_lower:

        strengths.append(
            "Experience detected"
        )

    else:

        weaknesses.append(
            "Add internship or experience"
        )


    return strengths, weaknesses


def extract_contact_info(text):

    name = "Not Found"
    email = "Not Found"
    phone = "Not Found"


    email_match = re.search(
        r'[\w\.-]+@[\w\.-]+',
        text
    )

    if email_match:
        email = email_match.group()


    phone_match = re.search(
        r'\b\d{10}\b',
        text
    )

    if phone_match:
        phone = phone_match.group()


    ignored = [
        "contact",
        "profile",
        "summary",
        "objective",
        "resume",
        "curriculum vitae",
        "skills",
        "education",
        "experience",
        "projects",
        "certification"
    ]


    lines = text.split("\n")


    for line in lines:

        clean = line.strip()

        if not clean:
            continue


        if clean.lower() in ignored:
            continue


        if (
            len(clean.split()) <= 4
            and clean.replace(" ", "").isalpha()
        ):
            name = clean
            break


    return name, email, phone




# Improved NLP Job Matching

def analyze_job_match(resume_text, job_description):

    if job_description.strip() == "":
        return 0, [], []


    documents = [
        resume_text,
        job_description
    ]


    vectorizer = TfidfVectorizer(
        stop_words="english"
    )


    vectors = vectorizer.fit_transform(documents)


    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]


    match_score = int(similarity * 100)


    stop_words = {
        "the",
        "and",
        "with",
        "to",
        "of",
        "for",
        "in",
        "a",
        "an",
        "on",
        "is",
        "are",
        "this",
        "that"
    }


    resume_words = set(
        word.lower()
        for word in re.findall(r'\b[a-zA-Z]+\b', resume_text)
        if word.lower() not in stop_words
    )


    job_words = set(
        word.lower()
        for word in re.findall(r'\b[a-zA-Z]+\b', job_description)
        if word.lower() not in stop_words
    )


    matched = resume_words.intersection(job_words)


    missing = job_words.difference(resume_words)


    return (
        match_score,
        list(matched)[:15],
        list(missing)[:15]
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

        resume_text=resume_text

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
    
