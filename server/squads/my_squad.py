from flask import redirect, render_template, request

from server.database.tables import Users, Squads

def handle_my_squad(request):
    """
    Handler for the 'my squad' page
    """
    commander_name = request.cookies.get("name")
    user = Users.query.filter_by(commander_name=commander_name).first()
    
    if user is None or commander_name is None:
        return redirect("/auth/signin")
    
    squad = Squads.query.filter_by(id=user.squad_id).first()
    
    if squad is None or user.squad_id is -1:
        return redirect("/squads/create")
    
    return render_template(
        "private/squad_page.html",
        name=squad.sName,
        tag=squad.sTag
    )