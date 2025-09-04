from server.database.tables import Squads


def get_squad_id(squad_name: str) -> int:
    result = Squads.query.filter_by(sName=squad_name.lower()).first()
    if result is None:
        return -1
    else:
        return result.id