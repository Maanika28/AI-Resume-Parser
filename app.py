from flask import Flask, render_template, request
from parser import *
import re

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    result = {
        "name": "",
        "email": "",
        "phone": "",
        "education": [],
        "skills": []
    }

    score = 0
    feedback = ""
    job_match = 0

    if request.method == "POST":

        file = request.files["resume"]

        if file and file.filename != "":

            path = "resumes/" + file.filename
            file.save(path)

            text = extract_text(path)

            result = {
                "name": extract_name(text),
                "email": extract_email(text),
                "phone": extract_phone(text),
                "education": extract_education(text),
                "skills": extract_skills(text)
            }

            # Resume Score

            if result["name"] != "Not Found":
                score += 10

            if result["email"] != "Not Found":
                score += 10

            if result["phone"] != "Not Found":
                score += 10

            if len(result["education"]) > 0:
                score += 15

            skill_count = len(result["skills"])

            if skill_count >= 10:
                score += 20
            elif skill_count >= 5:
                score += 15
            elif skill_count >= 3:
                score += 10

            project_count = count_projects(text)

            if project_count >= 3:
                score += 10
            elif project_count >= 1:
                score += 5

            internship_count = count_internships(text)

            if internship_count >= 1:
                score += 10

            cert_count = count_certifications(text)

            if cert_count >= 2:
                score += 10
            elif cert_count >= 1:
                score += 5

            if has_github(text):
                score += 10

            if has_linkedin(text):
                score += 5

            score = min(score, 100)

            # Feedback

            if score >= 80:
                feedback = "Excellent Resume"
            elif score >= 60:
                feedback = "Good Resume"
            else:
                feedback = "Needs Improvement"

            # Job Match Score

            jd_text = request.form.get("job_description", "")

            if jd_text.strip():

                jd_skills = [
                    skill.strip().lower()
                    for skill in re.split(r'[\n,]+', jd_text)
                    if skill.strip()
                ]

                resume_skills = [
                    skill.strip().lower()
                    for skill in result["skills"]
                ]

                matched = len(
                    set(jd_skills) & set(resume_skills)
                )

                if len(jd_skills) > 0:
                    job_match = int(
                        (matched / len(jd_skills)) * 100
                    )

            print("========== RESUME ANALYSIS ==========")
            print("Name:", result["name"])
            print("Skills:", result["skills"])
            print("Resume Score:", score)
            print("Job Match:", job_match)
            print("====================================")

    return render_template(
        "index.html",
        result=result,
        score=score,
        feedback=feedback,
        job_match=job_match
    )

if __name__ == "__main__":
    app.run(debug=True)