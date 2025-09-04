from server.database.tables import Goals, database
from server.database.squad import get_squad_id
from server.constants import GOAL_TYPES

def create_goal(goal_type: str, squad_name: str, goal_name: str, target: int) -> str:
    if goal_type in GOAL_TYPES.keys:
        #valid
        squad_id = get_squad_id(squad_name)
        if squad_id != -1:
            #valid squad
            newGoal = Goals(
                squad_id=squad_id,
                goal_units=goal_type,
                progress_data={
                    'contributors': {
                        
                    },
                    'name': goal_name,
                    'target': target,
                    'progress_raw': 0
                }
            )
            database.session.add(newGoal) 
            database.session.commit()
            
            return 'OK'
        else:
            return 'No Squad'
    else:
        return 'Invalid Goal Type'