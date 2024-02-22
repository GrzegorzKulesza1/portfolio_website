from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from datetime import datetime
import os

from blueprints.amber.amber_routes import amber_project_bp
from blueprints.quiz.quiz_routes import quiz_project_bp
from blueprints.todo_list.todo_list_routes import db, todo_list_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///todo-lists.db")
db.init_app(app)
Bootstrap(app)

# Automatically injects the year variable to all templates
@app.context_processor
def inject_year():
    return dict(year=datetime.now().year)

# Displays the home page
@app.route('/')
def main_page():
    return render_template("index.html")

# Displays sections about me
@app.route('/o-mnie')
def about_me():
    return render_template('about_me.html')

# Displays the contact section
@app.route("/kontakt")
def contact_me():
    return render_template("contact_me.html")

# Displays the cookie policy page
@app.route("/polityka-cookie")
def cookie():
    return render_template('cookie_policy.html')

app.register_blueprint(amber_project_bp)
app.register_blueprint(quiz_project_bp)
app.register_blueprint(todo_list_bp)

if __name__ == "__main__":
    app.run(debug=False)
