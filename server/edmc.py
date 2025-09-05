from flask import jsonify, request
from server.database.tables import Users, Squads


def handle_cmdr_squad_lookup(request):
    commander_name = str(request.args.get("cmdr")).lower()
    
    commander = Users.query.filter_by(commander_name=commander_name).first()
    squad = Squads.query.filter_by(id=commander.squad_id).first()
    
    return jsonify({
        'squad_name': squad.sName,
        'squad_tag': squad.sTag
    })  