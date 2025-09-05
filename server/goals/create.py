from server.database.tables import Goals, database
from server.database.squad import get_squad_id
from server.constants import GOAL_TYPES
from flask import render_template, request

def handle_goal_create(request):
    if request.method == "GET":
        return render_template(
            "goals/create_goal.html",
            goal_types=GOAL_TYPES.keys(),
            squad_id=get_squad_id(request.cookies.get("squad_name")),
        )
    elif request.method == "POST":
        title = request.form.get("title")
        squad_id = request.form.get("squad_id")
        goal_type = request.form.get("goal_type")
        info = request.form.get("info")
        goal = float(request.form.get("goal"))

        goal_data = {
            "name": title,
            "contributors": 0,
            "units": goal_type,
            "goal": goal,
            "progress": 0,
            "percentage": 0,
            "info": info,
        }
        
        newGoal = Goals(
            squad_id=squad_id,
            goal_units=goal_type,
            progress_data=goal_data
        )
        
        database.session.add(newGoal)
        database.session.commit()
        
        return render_template(
            "goals/complete.html",
            goal_name=title
        )
