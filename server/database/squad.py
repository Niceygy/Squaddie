from server.database.tables import Squads


def get_squad_id(squad_name: str) -> int:
    result = Squads.query.filter_by(squad_name=squad_name).first()
    if result is None:
        return -1
    else:
        return result.id