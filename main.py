from flask import Flask, render_template, redirect, url_for, request
from ratemyprof import profLookup
from courses import get_courses
from syllabus import get_syllabus_info
import ast

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def home_page():

    if request.method == "POST":

        module = request.form.get("module")
        program = request.form.get("program")

        courses = get_courses(program, module)
        data = {}

        for course in courses[:10]:

            try:

                data[course] = {
                    "syllabus": get_syllabus_info(course),
                    "profs": profLookup(course)
                }

            except Exception as e:

                print(e)
                continue

        return redirect(url_for("show_results", module=module, program=program, data=data))

    return render_template("index.html")


@app.route('/results', methods=["GET"])
def show_results():

    data = ast.literal_eval(request.args["data"])
    program = request.args["program"]
    module = request.args["module"]

    return render_template("success.html", data=data, program=program, module=module)


if __name__ == "__main__":

    app.run(port=4000, debug=True)
