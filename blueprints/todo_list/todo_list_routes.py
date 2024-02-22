from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from random import randint
import time
import secrets
import os

todo_list_bp = Blueprint('todo_list', __name__, template_folder='templates')

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_KEY")
db = SQLAlchemy()

# Variable for temporary data. The variable has the structure:
# users = {"user": {"list_name": "#", "all_todo": [{"name": "#", "completed": False}, "creation_time": #,}
users = {}
list_name_placeholder = 'Lista 1'

# Database structure
class TodoList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    list_name = db.Column(db.String(250))
    name = db.Column(db.String(250))
    completed = db.Column(db.Boolean())


def clear_users(temporary_users):
    """The function is responsible for clearing temporary data after 24 hours."""
    now = time.time()
    to_delete = [user for user, data in temporary_users.items() if now-data["creation_time"] > 86400]
    for user in to_delete:
        del users[user]


@todo_list_bp.route("/lista-rzeczy-do-zrobienia")
def main_page():
    db.create_all()
    clear_users(users)

    # Grants a unique ID to each new user session. Allows multiple users to use the application at the same time.
    if "user_id" not in session:
        session["user_id"] = secrets.token_urlsafe(8)
        users[session["user_id"]] = {"list_name": list_name_placeholder, "all_todo": [], "creation_time": time.time()}

    # The try-except block is used when the user's browser session lasts longer than 24 hours.
    try:
        users[session["user_id"]]["list_name"]
    except KeyError:
        session["user_id"] = secrets.token_urlsafe(8)
        users[session["user_id"]] = {"list_name": list_name_placeholder, "all_todo": [], "creation_time": time.time()}

    current_user = session["user_id"]
    return render_template('todo_list/todo_list_main.html',
                           list_name=users[current_user]["list_name"], all_todo=users[current_user]["all_todo"])


# The function retrieves a new to-do item from the form in todo_list_main.html
@todo_list_bp.route('/lista-rzeczy-do-zrobienia/dodaj', methods=["POST"])
def add():
    current_user = session["user_id"]
    todo = request.form["new_todo"]  # retrieves the name of the new to-do from the form
    users[current_user]["all_todo"].append({"name": todo, "completed": False})  # adds a new to-do to the variable users

    # adds a new item to the database if the user provided their list name
    if users[current_user]["list_name"] != list_name_placeholder:
        db_entry = TodoList(list_name=users[current_user]["list_name"], name=todo, completed=False)
        db.session.add(db_entry)
        db.session.commit()
    return redirect(url_for('todo_list.main_page'))


# The function retrieves the changed to-do name from the form in edit.html
@todo_list_bp.route("/lista-rzeczy-do-zrobienia/edytuj/<int:index>", methods=["GET", "POST"])
def edit(index):
    current_user = session["user_id"]

    if request.method == "POST":
        # Based on the index it determines which to-do should be changed
        edited_todo = users[current_user]["all_todo"][index]
        edited_todo["name"] = request.form["new_name"]

        # saves the changes to the database if the user uses his list
        if users[current_user]["list_name"] != list_name_placeholder:
            # db_todos retrieves all entries of the current list from the database
            db_todos = TodoList.query.filter_by(list_name=users[current_user]["list_name"]).all()
            db_to_edit = db_todos[index]
            db_to_edit.name = request.form["new_name"]
            db.session.commit()

        return redirect(url_for("todo_list.main_page"))
    return render_template("todo_list/edit.html",
                           list_name=users[current_user]["list_name"],
                           all_todo=users[current_user]["all_todo"],
                           index=index)


# Function responsible for crossing out completed to-dos.
@todo_list_bp.route("/lista-rzeczy-do-zrobienia/sprawdz", methods=["GET", "POST"])
def checkbox_clicked():
    current_user = session["user_id"]
    edited_todos = users[current_user]["all_todo"]

    tasks_completed = request.form.getlist('completed')  # retrieves a list of all selected todos as index
    for index in tasks_completed:
        # changes the completed status to the opposite
        edited_todos[int(index)]["completed"] = not edited_todos[int(index)]["completed"]

    # if the user uses his list, it makes changes to the completed variable in the database
    if users[current_user]["list_name"] != list_name_placeholder:
        # db_todos retrieves all entries of the current list from the database
        db_todos = TodoList.query.filter_by(list_name=users[current_user]["list_name"]).all()
        for index in tasks_completed:
            db_todos[int(index)].completed = edited_todos[int(index)]["completed"]
            db.session.commit()
    return redirect(url_for('todo_list.main_page'))


# Function removes to-do.
@todo_list_bp.route("/lista-rzeczy-do-zrobienia/usun/<int:index>", methods=["GET", "POST"])
def delete(index):
    current_user = session["user_id"]
    # if the user uses his list, makes changes to the database.
    if users[current_user]["list_name"] != list_name_placeholder:
        # db_todos retrieves all entries of the current list from the database
        db_todos = TodoList.query.filter_by(list_name=users[current_user]["list_name"]).all()
        db_to_delete = db_todos[index]
        db.session.delete(db_to_delete)
        db.session.commit()
        # Renames the list to the default when all items from the database are deleted
        if len(db_todos) == 1:
            users[current_user]["list_name"] = list_name_placeholder
    del users[current_user]["all_todo"][index]
    return redirect(url_for('todo_list.main_page'))


# Retrieves the user-supplied list name from save_list.html and saves changes to the list_name variable
# and the database.
@todo_list_bp.route("/lista-rzeczy-do-zrobienia/zapisz-liste", methods=["GET", "POST"])
def save_list():
    if request.method == "POST":
        current_user = session["user_id"]
        new_name = request.form.get("new_list_name")
        new_name = new_name + '#' + str(randint(1000, 9999))
        users[current_user]["list_name"] = new_name

        # Adds all created todos to the database along with the name of the list
        for todo in users[current_user]["all_todo"]:
            db_entry = TodoList(list_name=new_name, name=todo['name'], completed=todo['completed'])
            db.session.add(db_entry)
            db.session.commit()

        return render_template('todo_list/save_list.html', name=new_name)
    return render_template('todo_list/save_list.html')


# Gets the entered list name from upload_list.html and retrieves it from the database.
# If the list name does not exist in the database, sends a flash message to upload_list.html.
@todo_list_bp.route('/lista-rzeczy-do-zrobienia/wczytaj-liste', methods=["GET", "POST"])
def upload_list():
    if request.method == "POST":
        user_list_name = request.form.get('list_name')
        user_list = TodoList.query.filter_by(list_name=user_list_name).all()
        # Checks whether the list name entered by the user exists in the database.
        if user_list:
            current_user = session["user_id"]
            users[current_user]["list_name"] = user_list_name
            users[current_user]["all_todo"].clear()
            users[current_user]["all_todo"] = [{"name": todo.name, "completed": todo.completed} for todo in user_list]
            return redirect(url_for('todo_list.main_page'))
        else:
            flash(user_list_name)  # Information that the list name provided by the user is not in the database

    return render_template('todo_list/upload_list.html')


# After clicking the New list button, it restores the starting values of the variables list_name and all_todo.
@todo_list_bp.route('/lista-rzeczy-do-zrobienia/nowa-lista')
def new_list():
    current_user = session["user_id"]
    users[current_user]["list_name"] = list_name_placeholder
    users[current_user]["all_todo"] = []
    return redirect(url_for('todo_list.main_page'))
