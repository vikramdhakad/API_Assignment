import fitz  # PyMuPDF
import re

def extract_resume_data(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    return {
        "name": extract_name(text),
        "about": {
            "bio": extract_about(text)
        },
        "contact": {
            "email": extract_email(text),
            "phone": extract_phone(text)
        },
        "skills": extract_skills(text),
        "experience": extract_experience(text),
        "education": extract_education(text)
    }

def extract_name(text):
    lines = text.strip().split('\n')
    if lines:
        first_line = lines[0].strip()
        if len(first_line.split()) <= 4:
            return first_line
    return "Name Not Detected"

def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else "Email Not Found"

def extract_phone(text):
    match = re.search(r'\+?\d[\d\s-]{7,}\d', text)
    return match.group(0) if match else "Phone Not Found"

def extract_about(text):
    lines = text.split('\n')
    about_lines = []
    capture = False
    stop_keywords = ['experience', 'education', 'project', 'certifications', 'skills', 'technical', 'work history', 'employment']
    start_keywords = ['summary', 'about', 'profile', 'objective', "bio", 'introduction', "CAREER SUMMARY:", "PROFESSIONAL SUMMARY:"]

    for i, line in enumerate(lines):
        lower_line = line.strip().lower()

        # Start capturing if a start keyword is found
        if any(keyword in lower_line for keyword in start_keywords):
            capture = True
            continue

        # Stop capturing when another section starts
        if capture and (any(stop in lower_line for stop in stop_keywords) or line.strip() == ''):
            break

        if capture:
            about_lines.append(line.strip())

    result = ' '.join(about_lines).strip()
    return result if result else "Bio not found"

def extract_skills(text):
    KNOWN_SKILLS = [
        "Python", "Flask", "SQL", "Pandas", "NumPy", "Power BI",
        "Excel", "JavaScript", "HTML", "CSS", "Git", "Django"
    ]
    found = []
    for skill in KNOWN_SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            found.append(skill)
    return found

def extract_experience(text):
    experience_keywords = [
        "Intern", "Developer", "Engineer", "Analyst", "Manager",
        "Consultant", "Company", "Worked at", "Experience"
    ]
    lines = text.split('\n')
    seen = set()
    result = []
    for line in lines:
        for keyword in experience_keywords:
            if keyword.lower() in line.lower() and line not in seen:
                seen.add(line)
                result.append(line.strip())
    return result

def extract_education(text):
    education_keywords = [
        "B.Tech", "M.Tech", "Bachelor", "Master", "B.Sc", "M.Sc",
        "Engineering", "Computer Science", "BCA", "MCA"
    ]
    lines = text.split('\n')
    seen = set()
    result = []
    for line in lines:
        for keyword in education_keywords:
            if keyword.lower() in line.lower() and line not in seen:
                seen.add(line)
                result.append(line.strip())
    return result