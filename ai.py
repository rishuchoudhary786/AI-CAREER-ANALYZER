from groq import Groq
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_resume(resume_text, user_goal):
    prompt = f"""
    You are an elite, highly rigorous Technical Recruiter and Senior Career Counselor.
    Analyze the following resume and provide an incredibly detailed, comprehensive feedback report based on the user's career goal.
    User goal: "{user_goal}"

    STRICT RULES FOR GENERATION:
    - Provide deep, descriptive paragraphs and multi-step bullet points containing 'from beginner to advanced' details.
    - Evaluate exactly how ready the user is for this role and provide a definitive 'Resume Score' out of 100 based on their current resume vs the industry standard.
    - Give a harsh, constructive critique ('Resume Feedback') on the structure, phrasing, and impact of the text.
    - Detail specific technical and soft skill gaps.
    - Propose tiered 'Project Ideas' (Beginner, Intermediate, Advanced) to help them build their missing skills.
    - Recommend top-tier industry 'Certifications' they should aim for.
    - Craft an exhaustive, multi-step 'Roadmap' breaking down exactly what they must learn to bridge the gap.
    - Formulate extreme, real-world 'Interview Preparation' questions scaling from basic fundamentals to advanced architecture scenarios.

    Return ONLY valid JSON, no extra text, no markdown backticks. All arrays MUST contain only strings, do NOT use objects:
    {{
        "resume_score": 85,
        "resume_feedback": ["Critique point 1 with deep detail...", "Critique point 2..."],
        "skills": ["skill 1", "skill 2"],
        "missing_skills": ["missing fundamental skill 1", "missing advanced skill 2"],
        "project_ideas": ["Beginner: Project name - description", "Advanced: Project name - description"],
        "certifications": ["Cert 1 - Why it matters", "Cert 2 - Why it matters"],
        "roadmap": ["Step 1 (Beginner): Detailed action plan...", "Step 2 (Advanced): Detailed action plan..."],
        "interview_preparation": ["Basic: Question 1?", "Advanced: Scenario Question 2?"]
    }}

    Resume:
    {resume_text}
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a specialized technical recruiter and career coach. Return ONLY valid JSON format."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        content = completion.choices[0].message.content.strip()

        return json.loads(content)

    except Exception as e:
        print(f"Groq API error: {e}")
        return {
            "error": f"Groq Processing Error: {str(e)}",
            "resume_score": 0,
            "resume_feedback": [],
            "skills": [],
            "missing_skills": [],
            "project_ideas": [],
            "certifications": [],
            "roadmap": [],
            "interview_preparation": []
        }