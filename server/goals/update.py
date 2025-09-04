from flask import jsonify

from server.database.squad import get_squad_id
from server.database.tables import Goals

def handle_update(request):
    """
    Update POST format:
    
    type=combat/trade profit/ect
    cmdr=niceygy (to lower!)
    units=66
    squad=soteria accord (to lower!)
    """
    goal_type = request.form.get("type")
    commander = request.form.get("cmdr")
    squad = request.form.get("squad")
    units = request.form.get("units")
    
    squad_id = get_squad_id(squad)
    
    goal = Goals.query.filter_by(squad_id=squad_id, goal_units=goal_type).first()
    
    if goal is not None:
        progress_data = goal.progress_data
        if commander in progress_data['contributors']:
            #they have contributed before, add it to their total
            progress_data['contributors'][commander] = progress_data['contributors'][commander] + units
        else:
            progress_data['contributors'][commander] = units
            
        Goals.query.session.commit()
        
        return jsonify({
            'response': "OK"
        })
    else:
        return jsonify({
            'response': "NOT_FOUND"
        })