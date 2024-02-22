from flask import Blueprint, render_template, request
from blueprints.amber import amber_logic

amber_project_bp = Blueprint('amber_project', __name__, template_folder='templates')

@amber_project_bp.route('/bursztyny', methods=["POST", "GET"])
def amber_page():
    if request.method == "POST":
        location = request.form["location"]
    else:
        location = "Wyspa Sobieszewska"

    amber = amber_logic.AmberBrain(location)
    amber.get_all_attributes()
    return render_template("amber/amber_main.html",
                           temperature=amber.avg_temperature,
                           speed=amber.avg_wind_speed,
                           is_strong=amber.wind_strong_enough,
                           direction=amber.is_good_direction,
                           city=amber.city)
