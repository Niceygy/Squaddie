from server.database.tables import Squads, Users


def does_user_exist(commander_name: str) -> bool:
    user = Users.query.filter_by(commander_name=commander_name).first()
    return user is not None

def create_new_user(commander_name: str, password_hash: str, squad_name: str) -> bool:
        #do they already exist?
    if not does_user_exist(commander_name):
        #no
        
        #find squad
        squad = Squads.query.filter_by(sName=squad_name).first()
        if not squad:
            return "squad_not_exists", False
        
        new_user = Users(
            commander_name=commander_name,
            squad_id=squad.id,
            password_hash=password_hash,
            progress_data={
                ''
            }
            
        
        )
    else:
        return "user_exists", False