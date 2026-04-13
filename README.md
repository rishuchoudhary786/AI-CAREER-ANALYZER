# AI-CAREER-ANALYZER
An intelligent Resume Evaluation and Career Mapping platform built with Python, Flask, and Llama-3 AI. Automatically parses resumes to generate tiered technical roadmaps, readiness scores, and project ideas based on career goals.

# 🚀 AI Career Analyzer

An intelligent, Glassmorphism-styled web application that acts as an elite generative AI Career Counselor. By parsing PDF resumes and leveraging the incredible speed of **Llama-3**, this platform instantly calculates a candidate's readiness score, identifies deep technical skill gaps, and generates a comprehensive, multi-tiered roadmap to help users secure their dream roles.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Framework-Flask-green.svg)
![TiDB](https://img.shields.io/badge/Database-TiDB-orange.svg)
![AI](https://img.shields.io/badge/LLM-Llama--3-purple.svg)

---

## ✨ Features

- **Deep PDF Text Parsing:** Extracts raw unstructured NLP texts from standard user resumes.
- **Definitive Resume Scoring (0-100%):** The AI algorithm calculates exactly how qualified you are for your specified target role.
- **Harsh Constructive Feedback:** Identifies structural and phrasing flaws directly within your resume.
- **Tiered Project Ideas & Certifications:** Recommends industry-recognized certifications and portfolio projects scaled from Beginner to Advanced.
- **Historical Database Syncing:** Saves all generated analytics into a persistent TiDB cloud database, allowing you to review past reports visually.
- **Premium UX/UI:** Designed with a sleek Dark Blue Glassmorphism aesthetic, featuring animated Flash Toasts, staggered cascading grid reveals, and immersive AJAX loading screens.

## 🛠️ Technology Stack

- **Backend:** Python, Flask, SQLAlchemy ORM
- **Database:** TiDB (Distributed SQL Cloud)
- **AI Integration:** Groq API (Running `llama-3.3-70b-versatile`)
- **Frontend:** HTML5, CSS3, Vanilla JS
- **Parser:** PyPDF2

---

## 🏃‍♂️ Quick Start (Installation)

To run this project locally on your machine, follow these steps:

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ai-career-analyzer.git
cd ai-career-analyzer
```

### 2. Set Up the Virtual Environment
```bash
python -m venv venv
.\venv\Scripts\activate   # On Windows
# source venv/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies
```bash
pip install flask sqlalchemy pymysql python-dotenv PyPDF2 groq
```

### 4. Configure Environment Variables
Create a file exactly named `.env` in the root folder and add your private credentials. **(Never upload this file to GitHub!)**
```env
GROQ_API_KEY=your_groq_llama_key_here
TIDB_HOST=your_tidb_host
TIDB_PORT=4000
TIDB_USER=your_username.root
TIDB_PASSWORD=your_database_password
TIDB_DB=test
```

### 5. Initialize the Database & Run
```bash
# This builds the tables in the database
python init_db.py

# This starts the backend Flask server
python app.py
```
**Access the platform at: `http://127.0.0.1:5000`**

---
*If you need a deep, academic breakdown of the architectural flow and database schemas, please read the included `PROJECT_REPORT.md` file.*
