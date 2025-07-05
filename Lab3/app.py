import sys
import jinja2
from matplotlib import pyplot as plt


STUDENT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Details</title>
    </head>
<body>
    <h1>Student Details</h1>
    <table border="1">
        <tr>
            <th>Student id</th>
            <th>Course id</th>
            <th>Marks</th>
        </tr>
        {% for student in students %}
            <tr>
                <td>{{ student.student_id }}</td>
                <td>{{ student.course_id }}</td>
                <td>{{ student.marks }}</td>
            </tr>
        {% endfor %}
        <tr>
            <td colspan="2">Total Marks</td>
            <td> {{ total_marks }} </td>
        </tr>
    </table>
</body>
</html>
"""


COURSE_TEMPLATE = """

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Course Details</title>
</head>
<body>
    <h1>Course Details</h1>
    <table border="1">
        <tr>
            <th>Average Marks</th>
            <th>Maximum Marks</th>
        </tr>
        <tr>
            <td>{{ average_marks }}</td>
            <td>{{ highest_marks }}</td>
        </tr>
    </table>
    <img src="{{ img }}" alt="Histogram of Marks" height="350" width="450" align="left" valign="top">
</body>
</html>
"""

ERROR_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error</title>
</head>
<body>
    <h1>Wrong Inputs</h1>
    <p>Something went wrong</p>
</body>
</html>
"""


def render_template(template, context):
    """Render the given template with the provided context."""
    template = jinja2.Template(template)
    return template.render(**context)


def write_output(output):
    """Write the rendered output to output.html."""
    with open("output.html", "w") as f:
        f.write(output)



def main():
    try:
        if len(sys.argv) <= 2 or sys.argv[1] not in ['-s', '-c']:
            raise ValueError("Invalid arguments")

        flag = sys.argv[1]
        target_id = sys.argv[2]

        # Read the CSV file
        try:
            with open("data.csv", "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            raise ValueError("data.csv file not found")

        # Validate header
        header = [col.strip() for col in lines[0].split(",")]
        if header != ['Student id', 'Course id', 'Marks']:
            raise ValueError("Invalid CSV header format")

        output = None
        
        # Checking the data for the student
        if flag == '-s':
            students = []
            total_marks = 0

            
            for line in lines[1:]:
                parts = [x.strip() for x in line.strip().split(',')]
                if len(parts) != 3:
                    raise ValueError("Invalid line format in CSV")

                
                student_id, course_id, marks = parts
                if student_id == target_id:
                    students.append({
                        'student_id': student_id,
                        'course_id': course_id,
                        'marks': marks
                    })
                    total_marks += int(marks)

            
            if not students:
                raise ValueError("No data for student")

            context = {'students': students, 'total_marks': total_marks}
            output = render_template(STUDENT_TEMPLATE, context)

        # Checking the data for the course
        elif flag == '-c':
            marks_list = []
            total_marks = 0
            highest_marks = 0

            
            for line in lines[1:]:
                parts = [x.strip() for x in line.strip().split(',')]
                if len(parts) != 3:
                    raise ValueError("Invalid line format in CSV")
                
                
                student_id, course_id, marks = parts
                if course_id == target_id:
                    marks = int(marks)
                    marks_list.append(marks)
                    total_marks += marks
                    if marks > highest_marks:
                        highest_marks = marks
            
            # If no course found with the given id, raise an error
            if not marks_list:
                raise ValueError("No data for course")

            average_marks = total_marks / len(marks_list)

            # Plot the histogram
            plt.hist(marks_list, bins=10, edgecolor='black')
            plt.xlabel("Marks")
            plt.ylabel("Frequency")
            plt.title("Histogram of Marks")
            plt.savefig("histogram.png", dpi=300)
            plt.close()

            context = {
                'average_marks': round(average_marks, 2),
                'highest_marks': highest_marks,
                'img': 'histogram.png'
            }
            output = render_template(COURSE_TEMPLATE, context)

    except Exception:
        output = render_template(ERROR_TEMPLATE, {})

    # Return the output to be written to the file
    finally:
        if output is None:
            output = render_template(ERROR_TEMPLATE, {})
        return output


if __name__ == "__main__":
    output = main()
    if output:
        write_output(output)
