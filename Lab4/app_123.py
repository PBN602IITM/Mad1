from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        id_type = request.form.get("ID")
        id_value = request.form.get("id_value")
        df = pd.read_csv("data.csv")
        print(id_type,id_value)
        if not id_type or not id_value or not id_value.strip():
            return render_template("error.html", message="ID type or value missing.")

        if id_type == "student_id":
            if not id_value.isdigit():
                return render_template("error.html", message="Invalid Student ID entered.")
            student_data =df.loc[ df["Student ID"] == id_value]
            if student_data.empty:
                return render_template("error.html", message="No data found for this Student ID.")
            total_marks = student_data["Marks"].sum()
            return render_template("student_details.html",
                                   tables=student_data.to_dict(orient='records'),
                                   total=total_marks)

        elif id_type == "course_id":
            if not id_value.isdigit():
                return render_template("error.html", message="Invalid Course ID entered.")
            course_data = df.loc[df["Course ID"] == int(id_value)]
            if course_data.empty:
                return render_template("error.html", message="No data found for this Course ID.")
            avg_marks = round(course_data["Marks"].mean(), 2)
            max_marks = course_data["Marks"].max()

            plt.figure()
            plt.hist(course_data["Marks"], bins=10, edgecolor='black')
            plt.title(f"Histogram for Course ID: {id_value}")
            plt.xlabel("Marks")
            plt.ylabel("Frequency")

            if not os.path.exists("static"):
                os.makedirs("static")
            plot_path = f"static/hist_{id_value}.png"
            plt.savefig(plot_path)
            plt.close()

            return render_template("course_details.html",
                                   avg=avg_marks,
                                   max=max_marks,
                                   plot_url=plot_path)

        else:
            return render_template("error.html", message="Invalid ID type selected.")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)