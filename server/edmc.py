from flask import jsonify, render_template, request
from server.database.tables import Users, Squads, PluginLastSeen, database
from datetime import datetime


def handle_cmdr_squad_lookup(request):
    commander_name = str(request.args.get("cmdr")).lower()
    
    commander = Users.query.filter_by(commander_name=commander_name).first()
    if commander is None:
        return jsonify({'error': 'Commander not found'}), 404
    squad = Squads.query.filter_by(id=commander.squad_id).first()
    if squad is None:
        return jsonify({'error': 'Squad not found'}), 404
    
    return jsonify({
        'squad_name': squad.sName,
        'squad_tag': squad.sTag
    })  
    
def handle_plugin_find_lastseen(request):
    """
    Returns the last time the plugin was seen, if at all
    """
    commander_name = request.cookies.get("name")
    lastSeen = PluginLastSeen.query.filter_by(cmdr_name=commander_name).first()
    
    if lastSeen is None:
        return render_template(
            "squad/plugin_check.html",
            plugin_status="Not Found",
            plugin_last_seen="... Never"
        )
    else:
        return render_template(
            "squad/plugin_check.html",
            plugin_status="Connected",
            plugin_last_seen=lastSeen.time
        )
        
def handle_plugin_online(request):
    commander_name = str(request.args.get("cmdr")).lower()
    
    lastSeen = PluginLastSeen.query.filter_by(cmdr_name=commander_name).first()
    
    if lastSeen is None:
        newLastSeen = PluginLastSeen(
            cmdr_name=commander_name,
            time=datetime.now()
        )
        database.session.add(newLastSeen)
    else:
        lastSeen.time = datetime.now()
    
    database.session.flush()
    database.session.commit()
    
    return 'OK'