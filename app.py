from fileinput import filename

from flask import Flask, render_template, request, redirect, session, flash
from ai import analyze_resume
from db import Base, engine, sessionLocal
import models 
import PyPDF2
import docx
import json


app = Flask(__name__)
app.secret_key = 'secret 1234'

Base.metadata.create_all(bind=engine)  

#HOME
@app.route('/')
def home():
    if 'user' in session:
        return redirect('/dashboard')
    return redirect('/login')

#--------SIGNUP

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    db = sessionLocal()

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        existing_user = db.query(models.User).filter(models.User.email == email).first()

        if existing_user:
            flash("User already exists! Please login.", "error")
            return redirect('/signup')

        new_user = models.User(name=name, email=email, password=password)
        db.add(new_user)
        db.commit()
        db.close()

        return redirect('/login')
    
    return render_template('/signup.html')


#-------LOGIN


@app.route('/login', methods=['GET', 'POST'])
def login():
    db = sessionLocal()

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = db.query(models.User).filter(models.User.email == email, models.User.password == password).first()

        if user and user.password == password:
            session['user'] = user.id
            flash("Login Successful! Welcome back.", "success")
            return redirect('/dashboard')
        else:
            flash("Invalid Email or Password", "error")
            return redirect('/login')

    return render_template('login.html')

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        new_password = request.form.get('new_password')
        
        db = sessionLocal()
        user = db.query(models.User).filter_by(email=email).first()
        
        if user:
            user.password = new_password
            db.commit()
            flash("Password updated successfully! You can now login.", "success")
            return redirect('/login')
        else:
            flash("No account matches that email address.", "error")
            return redirect('/reset-password')

    return render_template('reset_password.html')


#-------DASHBOARD
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    db = sessionLocal()
    user = db.query(models.User).filter_by(id=session['user']).first()

    result=None

    if request.method == 'POST':
        user_goal = request.form.get('role')
        resume_text = request.form.get('resume')
        
        file = request.files.get('file')

        #file handling
        if file and file.filename != '':
            if file.filename.endswith('.pdf'):
                try:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ''
                    for page in pdf_reader.pages:
                        text += page.extract_text() or ''
                        resume_text = text
                except Exception as e:
                    result = {"error": f"PDF error: {str(e)}"}

            elif file.filename.endswith('.docx'):
                try:
                    doc = docx.Document(file)
                    text = '\n'.join([para.text for para in doc.paragraphs])
                    resume_text = text

                except Exception as e:
                    result = {"error": f"DOCX error: {str(e)}"}
            else:
                return "Unsupported file format"
        if resume_text and user_goal:
            try:    
                result = analyze_resume(resume_text, user_goal)


#----save to db

                report = models.Reports(user_id=user.id, resume_text=resume_text, result=json.dumps(result))
                db.add(report)
                db.commit()

            except Exception as e:
                    result = {"error": f"AI error: {str(e)}"} 
  
    return render_template('dashboard.html', user=user.name, result=result)


#---history
@app.route('/history')
def history():
    if 'user' not in session:
        return redirect('/login')

    db = sessionLocal()
    user = db.query(models.User).filter_by(id=session['user']).first()

    reports = db.query(models.Reports).filter_by(user_id=user.id).order_by(models.Reports.id.desc()).all()

    #convert json string into dict
    pasred_report = [] 
    for r in reports:
        try:
           pasred_result = json.loads(r.result)
        except:
            pasred_result = []

        pasred_report.append({
            "resume": r.resume_text,
            "result": pasred_result
        })

          
    return render_template('history.html', reports=pasred_report)


#LOGOUT
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')



if __name__ == '__main__':
    app.run(debug=True)