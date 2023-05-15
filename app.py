from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "asdf"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []


@app.route("/")
def begin_survey():
    """Survey home page"""
    return render_template("begin_survey.html", survey=survey)


@app.route("/begin", methods=["POST"])
def goto_survey():
    """initialise the survey"""
    return redirect("/questions/0")


@app.route("/questions/<int:q_num>")
def ask_question(q_num):
    """Ask The current question"""
    if len(responses) == len(survey.questions):
        return redirect("/thanks")
    if len(responses) != q_num:
        flash(f"{q_num} is not a valid question number")
        return redirect(f"/questions/{len(responses)}")
    question = survey.questions[q_num]
    return render_template("question.html", q_num=q_num, question=question)


@app.route("/submit", methods=["POST"])
def handle_response():
    """Records the users answers"""
    # responses.append(request.form["choice"])
    responses.append(request.form["choice"])
    if len(responses) == len(survey.questions):
        return redirect("/thanks")
    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/thanks")
def thanks():
    """thank the user for taking the survey"""
    return render_template("thanks.html")
