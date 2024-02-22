from flask import Blueprint, render_template, request, redirect, url_for
from blueprints.quiz import quiz_logic

quiz_project_bp = Blueprint('quiz_project', __name__, template_folder='templates', static_folder='static')

# Responsible for displaying the Quiz start page and retrieving data from the form
@quiz_project_bp.route("/quiz", methods=["GET", "POST"])
def quiz_page():
    form = quiz_logic.QuizForm()
    if form.validate_on_submit():
        num_of_questions = form.num_of_questions.data
        category = form.category.data
        quiz = quiz_logic.SetUpQuiz(num_of_questions, category)
        question_ids = quiz.question_ids
        return redirect(url_for("quiz_project.quiz_brain", ids=question_ids))
    return render_template("quiz/quiz_main.html", form=form)

# Responsible for displaying questions and retrieving answers provided by the User
@quiz_project_bp.route("/quiz/<ids>", methods=["POST", "GET"])
def quiz_brain(ids):
    game = quiz_logic.QuizGame(ids)  # Prepares questions and all answers for the Quiz
    all_questions = game.list_of_questions
    list_of_answers = []
    score = 0
    # Retrieves all answers entered by the User
    if request.method == "POST":
        for num in range(len(all_questions)):
            data = request.form.get("question-" + str(num))
            list_of_answers.append(data)
            if data == all_questions[num].right_answer:  # Checks how many correct answers the User had
                score += 1
        return render_template("quiz/quiz_game.html", all_questions=all_questions,
                               choices=list_of_answers, score=score)
    return render_template("quiz/quiz_game.html", all_questions=all_questions)
