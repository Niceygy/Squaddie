import math
from server.database.tables import Goals, Contributions
from server.constants import GOAL_UNITS


def get_total_goal_data(squad_id: int):
    goal = Goals.query.filter_by(squad_id=squad_id).first()
    
    contributions = Contributions.query.filter_by(goal_id=goal.id, squad_id=squad_id).all()
    
    players = 0
    qty = 0
    
    
    for item in contributions:
        qty += item.quantity
        players += 1
        

    return {
        'name': goal.progress_data['name'],
        'contributors': players,
        'units': GOAL_UNITS[goal.goal_units],
        'type': goal.goal_units,
        'goal': goal.progress_data['goal'],
        'progress': qty,
        'info': goal.progress_data['info'],
        'bars': math.trunc((( qty / int(goal.progress_data['goal'])) * 100) / 10)
    }