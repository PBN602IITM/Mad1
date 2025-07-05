import sys ,os
from flask import Flask,  render_template, request, url_for
from matplotlib import pyplot as plt

app = Flask(__name__)
path, dummy = os.path.split(os.path.realpath(__file__))

@app.route("/", methods =["GET","POST"])
# @app.route("/home")
# @app.route("/index")
def home():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        choice = request.form["ID"]
        value = request.form["id_value"]
        #path, filename = os.path.split(os.path.realpath(__file__))
        #print(os.path , os.path.join(path,"static","data.csv"))
        try:
            with open(os.path.join(path,"data.csv"), "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            raise ValueError("data.csv file not found")

        # Validate header
        header = [col.strip() for col in lines[0].split(",")]
        if header != ['Student id', 'Course id', 'Marks']:
            raise ValueError("Invalid CSV header format")
        # print (choice,value)
        if choice == "student_id":
            return student(value,lines)
        elif choice == "course_id":
            return course(value,lines)
        else:
            return render_template("Error_template.html")
        
    else:
        return render_template("Error_template.html")

def student(id,lines):
    students = []
    total_marks = 0

    for line in lines[1:]:
        #print(line)
        parts = [x.strip() for x in line.strip().split(',')]
        if len(parts) != 3:
            return render_template("Error_template.html")

        
        student_id, course_id, marks = parts
        if student_id == id:
            students.append({
                'student_id': student_id,
                'course_id': course_id,
                'marks': marks
            })
            total_marks += int(marks)
    
    if not students:
        return render_template("Error_template.html")

    context = {'students': students, 'total_marks': total_marks}
    return render_template("Student_template.html",students = students,total_marks=total_marks)

def course(id,lines):
    marks_list = []
    total_marks = 0
    highest_marks = 0


    for line in lines[1:]:
        parts = [x.strip() for x in line.strip().split(',')]
        if len(parts) != 3:
            raise ValueError("Invalid line format in CSV")
        
        
        student_id, course_id, marks = parts
        if course_id == id:
            marks = int(marks)
            marks_list.append(marks)
            total_marks += marks
            if marks > highest_marks:
                highest_marks = marks

    # If no course found with the given id, raise an error
    if not marks_list:
        return render_template("Error_template.html")

    average_marks = total_marks / len(marks_list)

    # Plot the histogram
    plt.hist(marks_list, bins=10, edgecolor='black')
    plt.xlabel("Marks")
    plt.ylabel("Frequency")
    plt.title("Histogram of Marks")
    plt.savefig(os.path.join(path,"static","histogram.png"), dpi=300)
    plt.close()

    x = url_for("home")
    print("url:" , os.path.join("static","histogram.png"))

#as
    return render_template("Course_template.html" ,average_marks=average_marks,highest_marks=highest_marks,img="static\\histogram.png")
    # return render_template("Course_template.html" ,average_marks=average_marks,highest_marks=highest_marks,img=os.path.join("static","histogram.png"))




if __name__ == "__main__":
    app.run(debug=True)
    