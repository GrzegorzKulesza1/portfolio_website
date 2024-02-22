from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import NumberRange
import csv
import random


class QuizForm(FlaskForm):
    """The class responsible for creating the Quiz form"""
    num_of_questions = IntegerField("Liczba pytań", validators=[NumberRange(3, 15)], default=5)
    category = SelectField("Kategoria", choices=["Wiedza Ogólna", "Filmy", "Gry Wideo", "Zwierzęta"],
                           default="Wiedza Ogólna")
    submit = SubmitField("Start")


class Question:
    """The class is responsible for creating objects from randomly chosen questions"""
    def __init__(self, q_id, q_text, q_answers, q_correct_ans):
        self.id = q_id
        self.text = q_text
        self.answers = q_answers
        self.right_answer = q_correct_ans


class SetUpQuiz:
    """The class responsible for preparing the Quiz. After the user selects the category and number of questions,
     it selects random questions and creates a list of question_ids."""
    def __init__(self, num_of_questions: int, choice: str):
        self.choice = choice
        self.num_of_questions = num_of_questions
        self.question_ids = ""

        with open("blueprints/quiz/static/question_data.csv", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            all_questions = [row for row in reader if row["category"] == self.choice]

        random_questions = random.sample(all_questions, self.num_of_questions)

        for question in random_questions:
            self.question_ids += question["id"] + "#"


class QuizGame:
    """The class takes question_ids from the SetUpQuiz class and creates a list of question objects."""
    def __init__(self, question_ids):
        self.numbers = question_ids.split("#")[:-1]
        self.list_of_questions = []

        with open("blueprints/quiz/static/question_data.csv", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            question_num = 0
            for row in reader:
                if row["id"] in self.numbers:
                    self.list_of_questions.append(Question(q_id=question_num,
                                                           q_text=row["text"],
                                                           q_answers=row["answers"].split("-")[:-1],
                                                           q_correct_ans=row["correct_answer"]))
                    question_num += 1
