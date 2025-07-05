from flask import Flask , render_template , request, redirect, url_for
import os   
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Table 1: student
class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)

# Table 2: course
class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)

# Table 3: enrollments
class Enrollments(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estudent_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    ecourse_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)

@app.route("/")
def home():
    students = Student.query.all()  # Fetch all students from the database
    return render_template("home.html" , students=students)

@app.route("/student/create" , methods=["GET", "POST"])
def create_student():
    if request.method == "POST":
        roll_number = request.form.get("roll")
        student = Student.query.filter_by(roll_number=roll_number).first()
        if not student:
            first_name = request.form.get("f_name")
            last_name = request.form.get("l_name")
            courses = request.form.getlist("courses")

            new_student = Student(roll_number=roll_number, first_name=first_name, last_name=last_name)
            db.session.add(new_student)
            db.session.flush()

            if courses:
                for course_id in courses:
                    enrollment = Enrollments(estudent_id=new_student.student_id, ecourse_id=int(course_id[-1]))
                    db.session.add(enrollment)

            db.session.commit()

            return redirect(url_for('home'))
        else:
            # If the student already exists, you can handle it as needed (e.g., show an error message)
            return render_template("student_exists.html")
    elif request.method == "GET":
        # Render the form for creating a new student
        return render_template("create_student.html")
    

@app.route("/student/<int:student_id>")
def student_detail(student_id):

    student = Student.query.filter_by(student_id=student_id).first()
    courses = db.session.query(Course).\
    join(Enrollments, Course.course_id == Enrollments.ecourse_id).\
    filter(Enrollments.estudent_id == student_id).all()
    return render_template("student_detail.html", student=student , courses=courses)

@app.route("/student/<int:student_id>/update", methods=["GET", "POST"])
def update_student(student_id): 
    student = Student.query.filter_by(student_id=student_id).first()
    if request.method == "POST":
        student.first_name = request.form.get("f_name")
        student.last_name = request.form.get("l_name")
        courses = request.form.getlist("courses")  
        # Clear existing enrollments for the student
        Enrollments.query.filter_by(estudent_id=student_id).delete()
        # Add new enrollments based on the selected courses
        if courses:
            for course_id in courses:
                enrollment = Enrollments(estudent_id=student.student_id, ecourse_id=int(course_id[-1]))
                db.session.add(enrollment) 
        db.session.commit()
        return redirect(url_for('student_detail', student_id=student.student_id))
    elif request.method == "GET":
        # Render the form for updating the student
        if not student:
            return "Student not found", 404
    # Render the form for updating the student
        courses = db.session.query(Course).\
        join(Enrollments, Course.course_id == Enrollments.ecourse_id).\
        filter(Enrollments.estudent_id == student_id).all()
        course_names = [course.course_name for course in courses]
        return render_template("update_student.html", student=student , course_names=course_names)
    

@app.route("/student/<int:student_id>/delete")
def delete_student(student_id):
    student = Student.query.filter_by(student_id=student_id).first()
    if student:
        db.session.delete(student)
        # Clear existing enrollments for the student
        Enrollments.query.filter_by(estudent_id=student_id).delete()
        db.session.commit()
    return redirect(url_for('home'))

        
if __name__ == "__main__":
    app.run(debug=True, port=5000)  # Run the Flask application