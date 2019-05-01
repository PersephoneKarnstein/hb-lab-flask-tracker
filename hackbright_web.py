"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, session, redirect

import hackbright

app = Flask(__name__)
app.secret_key = "OMGSOSECRETAAAAAA"

@app.route("/proj_redirect/<project_name>")
def do_redirect(project_name):
    return redirect("/project?<project_name>", 
                    # project_name = project_name,
                    code=303
                    )

@app.route("/student/<github>", methods=['GET', 'POST'])
def get_student(github):
    """Show information about a student."""

    # github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)
    grades = hackbright.get_grades_by_github(github)
    session[github] = {"first":first, "last":last, "github":github}



    return render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           grades=grades)


@app.route("/student_search")
def get_student_form():
    return render_template("student_search.html")


@app.route("/student_add")
def student_add():
    """Add a student."""

    return render_template('student_add.html')


@app.route("/student_add_success", methods=["POST", "GET"])
def student_add_success():

    first = request.form.get('fname')
    last = request.form.get('lname')
    github = request.form.get('github')

    print("\n\n\n\n\n\n\n", first, last, github, "\n\n\n\n\n\n\n")

    session[github] = {"first":first, "last":last, "github":github}

    hackbright.make_new_student(first, last, github)

    first, last, github = session[github].values()

    return render_template("student_add_success.html",
                                fname = first,
                                lname = last,
                                github = github
                                )

@app.route("/project", methods=['GET'])
def show_project():
    """List information about a project"""

    project_title = request.args.get("title")

    row = hackbright.get_project_by_title(project_title)

    student_proj_dict = dict()
    for student in hackbright.get_all_students():
        grades_by_title = hackbright.get_grades_by_title(project_title)
        for student_github, grade in grades_by_title:
            fname, lname, student_github = hackbright.get_student_by_github(student_github)
            l=locals()
            student_proj_dict[student_github] = {item:l[item] for item in\
             ["student_github", "fname", "lname", "grade"]}

    print("\n\n\n\n\n\n\n",student_proj_dict, "\n\n\n\n\n\n\n")


    return render_template("student_project.html", 
                            title = row[0],
                            description = row[1],
                            max_grade = row[2],
                            students = student_proj_dict
                            )


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
