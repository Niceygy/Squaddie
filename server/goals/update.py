from flask import jsonify
import hashlib

from server.database.squad import get_squad_id
from server.database.tables import Goals, Users

def handle_update(request):
    """
    Update POST format:
    
    type=combat/trade profit/ect
    commander_identifier=niceygy
    units=66
    """
    
    if 'event' in request.form:
        return
    
    goal_type = request.form.get("type")
    units = request.form.get("units")
    commander_name = request.form.get("commander_identifier")
    

    user = Users.query.filter_by(commander_name=commander_name).first()
    
    commander_name = user.commander_name
    squad_id = user.squad_id
    
    goal = Goals.query.filter_by(squad_id=squad_id, goal_units=goal_type).first()
    
    if goal is not None:
        progress_data = goal.progress_data
        if commander_name in progress_data['contributors']:
            #they have contributed before, add it to their total
            progress_data['contributors'][commander_name] = progress_data['contributors'][commander_name] + units
        else:
            progress_data['contributors'][commander_name] = units
            
        Goals.query.session.commit()
        
        print("OK")
        
        return jsonify({
            'response': "OK"
        })
    else:
        
        
        return jsonify({
            'response': "NOT_FOUND"
        })