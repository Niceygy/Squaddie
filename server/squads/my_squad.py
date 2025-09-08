from flask import redirect, render_template, request

from server.constants import GOAL_MESSAGE_TEMPLATE, GOAL_MESSAGES
from server.database.tables import Goals, Users, Squads
from server.goals.contrubutions import get_total_goal_data

def get_squad_members(squad_name: str) -> list:
    squad = Squads.query.filter_by(sName=squad_name).first()
    if squad is None:
        return []
    
    users = Users.query.filter_by(squad_id=squad.id).all()
    
    result = []
    
    for cmdr in users:
        result.append(cmdr.commander_name)
        
    return result

def handle_my_squad(request):
    """
    Handler for the 'my squad' page
    """
    commander_name = request.cookies.get("name")
    user = Users.query.filter_by(commander_name=commander_name).first()
    
    if user is None or commander_name is None:
        return redirect("/auth/signin")
    
    squad = Squads.query.filter_by(id=user.squad_id).first()
    
    if squad is None or user.squad_id == -1:
        return redirect("/squads/create")
    
    # goal_data = {
    #     'name': "Example Goal!",
    #     'contributors': 5,
    #     'units': "combat bonds",
    #     'goal': 500,
    #     'progress': 150,
    #     'percentage': (150 / 500) * 100,
    #     'info': "We need to kill pirates!"
    # }
    
    goal = Goals.query.filter_by(squad_id=squad.id).first()
    goal_data = get_total_goal_data(squad.id)
    # if goal is not None:

        
    
    return render_template(
        "squad/my_squad.html",
        name=squad.sName,
        tag=squad.sTag,
        owner=squad.sOwner,
        goal_data=goal_data,
        help_message=f"{GOAL_MESSAGE_TEMPLATE} {GOAL_MESSAGES[goal_data['type']]}",
        members=get_squad_members(squad.sName),
        contributors=goal_data['contributors']
    )