# Import necessary libraries
import sys
import jinja2
from matplotlib import pyplot as plt


"""

Simple python application to generate HTML reports based on student and course data
The application reads data from a CSV file named 'data.csv' and generates HTML reports for student details or course details based on the provided flags.
The application uses Jinja2 for templating and Matplotlib for generating histograms of marks.
The generated HTML content is saved to a file named 'output.html'.
The application handles errors gracefully by rendering an error page if the input is invalid or if no data is found for the given student or course id.
The application can be run from the command line with the following flags:
- `-s <student_id>`: To generate a report for a specific student by their id.
- `-c <course_id>`: To generate a report for a specific course by its id.
The variable output will contain the rendered HTML content based on the command line arguments provided.

"""

# Template for generating output.html with valid Student_data,
# runs if -s flag is provided with a valid student id
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

# Template for generating an HTML file with Course Details,
# run if -c flag is provided with a valid course id.

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

# Template for error page
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

# helper functions

# Function to render the template with the provided context
def render_template(template, context):
    """Render the given template with the provided context."""
    template = jinja2.Template(template)
    return template.render(**context)

# Function to write the rendered output to output.html
def write_output(output):
    """Write the rendered output to output.html."""
    with open("output.html", "w") as f:
        f.write(output)


# main logic starts here
def main():
    try:
        # Validate command-line arguments
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

            # Process each line in the CSV file while checking for valid format
            for line in lines[1:]:
                parts = [x.strip() for x in line.strip().split(',')]
                if len(parts) != 3:
                    raise ValueError("Invalid line format in CSV")

                # Extract student_id, course_id, and marks
                student_id, course_id, marks = parts
                if student_id == target_id:
                    students.append({
                        'student_id': student_id,
                        'course_id': course_id,
                        'marks': marks
                    })
                    total_marks += int(marks)

            # If no students found with the given id, raise an error
            if not students:
                raise ValueError("No data for student")

            context = {'students': students, 'total_marks': total_marks}
            output = render_template(STUDENT_TEMPLATE, context)

        # Checking the data for the course
        elif flag == '-c':
            marks_list = []
            total_marks = 0
            highest_marks = 0

            # Process each line in the CSV file while checking for valid format
            for line in lines[1:]:
                parts = [x.strip() for x in line.strip().split(',')]
                if len(parts) != 3:
                    raise ValueError("Invalid line format in CSV")
                
                # Extract student_id, course_id, and marks
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

    # Handle any exceptions that occur during processing
    except Exception:
        output = render_template(ERROR_TEMPLATE, {})

    # Return the output to be written to the file
    finally:
        # If output is None, it means an error occurred and the error page should be rendered
        if output is None:
            output = render_template(ERROR_TEMPLATE, {})
        return output


if __name__ == "__main__":
    output = main()
    # If output is not None, write it to output.html
    if output:
        write_output(output)
    # print("HTML file generated successfully: output.html")