from flask import redirect, render_template, request

from server.constants import GOAL_MESSAGE_TEMPLATE, GOAL_MESSAGES
from server.database.tables import Users, Squads
from server.goals.contrubutions import get_total_goal_data

def get_squad_members(squad_name: str) -> list:
    """Returns a list of all squad member's names

    Args:
        squad_name (str): Squadron name (lowercase)

    Returns:
        list: List of all squad members
    """
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
    
    goal_data = get_total_goal_data(squad.id)
    
    return render_template(
        "squad/my_squad.html",
        name=squad.sName,
        tag=squad.sTag,
        owner=squad.sOwner,
        goal_data=goal_data,
        help_message=f"{GOAL_MESSAGE_TEMPLATE} {GOAL_MESSAGES[goal_data['type']]}",
        members=get_squad_members(squad.sName),
        is_owner="true" if (squad.sOwner.lower() == commander_name.lower()) else "false",
        contributors=goal_data['contributors']
    )