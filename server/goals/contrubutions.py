from server.database.tables import Goals, Contributions


def get_total_goal_data(squad_id: int):
    goal = Goals.query.filter_by(squad_id=squad_id).first()
    
    contributions = Contributions.query.filter_by(goal_id=goal.id, squad_id=squad_id).all()
    
    players = 0
    qty = 0
    
    
    for item in contributions:
        qty += item.quantity
        players += 1
        
    # goal_data = {
    #     'name': "Example Goal!",
    #     'contributors': 5,
    #     'units': "combat bonds",
    #     'goal': 500,
    #     'progress': 150,
    #     'percentage': (150 / 500) * 100,
    #     'info': "We need to kill pirates!"
    # }
    return {
        'name': goal.pro
    }