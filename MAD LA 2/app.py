import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from jinja2 import Template

def main():
    arguments = sys.argv
    arguments.pop(0)
    df = pd.read_csv('./data.csv')
    
    if len(arguments) == 0:
        error()
        sys.exit()
        
    if arguments[0] == "-s":
        if len(arguments) == 1:
            error()
            sys.exit()
        write(s_data(df, arguments[1]))
        
    elif arguments[0] == "-c":
        if len(arguments) == 1:
            error()
            sys.exit()
        write(c_data(df, arguments[1]))
        
    else:
        error()
        sys.exit()

def s_data(df, sid):
    student_data = df.loc[df["Student id"] == int(sid)]
    
    if len(student_data) == 0:
        error()
        sys.exit()
        
    Total = student_data[" Marks"].sum()

    student_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Student Report</title>
        <style>
            table {
                border: 1px solid;
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid;
                padding: 8px;
            }
        </style>
    </head>
    <body>
        <h1>Student Details</h1>
        <table>
            <tr>
                <th>Student id</th>
                <th>Course id</th>
                <th>Marks</th>
            </tr>
            {% for row in student_data %}
            <tr>
                <td>{{ row['Student id'] }}</td>
                <td>{{ row[' Course id'] }}</td>
                <td>{{ row[' Marks'] }}</td>
            </tr>
            {% endfor %}
            <tr>
                <td colspan="2"><strong>Total Marks</strong></td>
                <td><strong>{{ Total }}</strong></td>
            </tr>
        </table>
    </body>
    </html>
    """
    template = Template(student_template)
    content = template.render(student_data=student_data.to_dict(orient="records"), Total=Total)
    return content
    print("Arguments:", arguments)

def c_data(df, cid):
    student_marks = df.loc[df[" Course id"] == int(cid)]
    
    if len(student_marks) == 0:
        error()
        sys.exit()
        
    average = student_marks[" Marks"].mean()
    max_marks = student_marks[" Marks"].max()
    
    plot(student_marks)

    course_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Course Report</title>
        <style>
            table {
                border: 1px solid;
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid;
                padding: 8px;
            }
        </style>
    </head>
    <body>
        <h1>Course Details</h1>
        <table>
            <tr>
                <th>Average Marks</th>
                <th>Maximum Marks</th>
            </tr>
            <tr>
                <td>{{ average }}</td>
                <td>{{ max_marks }}</td>
            </tr>
        </table>
        <h2>Marks Distribution</h2>
        <img src="bar-chart.png" height="250">
    </body>
    </html>
    """
    template = Template(course_template)
    content = template.render(average=average, max_marks=max_marks)
    return content

def error():
    error_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Error</title>
    </head>
    <body>
        <h1>Wrong Input</h1>
        <p>Please provide valid arguments like:</p>
        <ul>
            <li><code>python script.py -s &lt;student_id&gt;</code></li>
            <li><code>python script.py -c &lt;course_id&gt;</code></li>
        </ul>
    </body>
    </html>
    """
    template = Template(error_template)
    content = template.render()
    write(content)

def write(content):
    with open("output.html", "w") as f:
        f.write(content)
    print("Output written to output.html")

def plot(data):
    freq = data['Marks'].value_counts().sort_index()
    x = np.array(freq.index)
    
    lower_limit = (x.min() // 10) * 10
    
    plt.figure(figsize=(10, 6))
    plt.bar(x, freq.values, width=1, align='center', color='skyblue', edgecolor='black')
    
    plt.xlim(lower_limit, 100)
    plt.xticks(range(lower_limit, 101, 10))
    
    plt.xlabel('Marks')
    plt.ylabel('Frequency')
    plt.title('Marks Distribution')
    
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.savefig('bar-chart.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    main()
