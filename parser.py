import re
import PyPDF2


def extract_text(file_path):
    text = ""

    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            text = file.read()

    elif file_path.endswith(".pdf"):
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)

            for page in reader.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text

    # Clean PDF formatting issues
    text = text.replace(" @", "@")
    text = text.replace("@ ", "@")
    text = text.replace(". ", ".")
    text = text.replace("\n", " ")

    return text


def extract_name(text):
    lines = text.split()

    if len(lines) >= 2:
        return lines[0] + " " + lines[1]

    return "Not Found"


def extract_email(text):
    text = text.replace(" ", "")

    match = re.search(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        text
    )

    return match.group(0) if match else "Not Found"


def extract_phone(text):
    text = text.replace(" ", "")

    match = re.search(
        r'(\+91)?[6-9]\d{9}',
        text
    )

    return match.group(0) if match else "Not Found"


def extract_skills(text):
    skills_db = [
        "Python",
        "Java",
        "C",
        "C++",
        "SQL",
        "HTML",
        "CSS",
        "JavaScript",
        "Flask",
        "Django",
        "Machine Learning",
        "MySQL",
        "Git",
        "GitHub",
        "Linux",
        "DBMS",
        "REST API",
        "MATLAB"
    ]

    found = []

    for skill in skills_db:
        if skill.lower() in text.lower():
            found.append(skill)

    return found


def extract_education(text):
    education_keywords = [
        "B.E",
        "B.Tech",
        "Bachelor",
        "Engineering",
        "Computer Science",
        "Diploma",
        "MCA",
        "MBA"
    ]

    found = []

    for item in education_keywords:
        if item.lower() in text.lower():
            found.append(item)

    return found


def count_projects(text):
    keywords = [
        "project",
        "projects",
        "developed",
        "built",
        "implemented",
        "designed"
    ]

    count = 0

    for word in keywords:
        count += text.lower().count(word)

    return count


def count_internships(text):
    keywords = [
        "intern",
        "internship",
        "training",
        "work experience"
    ]

    count = 0

    for word in keywords:
        count += text.lower().count(word)

    return count


def count_certifications(text):
    keywords = [
        "certificate",
        "certification",
        "coursera",
        "udemy",
        "nptel",
        "aws",
        "google"
    ]

    count = 0

    for word in keywords:
        count += text.lower().count(word)

    return count


def has_github(text):
    return "github" in text.lower()


def has_linkedin(text):
    return "linkedin" in text.lower()