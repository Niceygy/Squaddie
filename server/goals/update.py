from flask import jsonify
import hashlib

from server.database.squad import get_squad_id
from server.database.tables import Goals, Users, Contributions
from server.database.tables import database


def handle_update(request):
    """
    Update POST format:

    type=combat/trade profit/ect
    commander_identifier=niceygy
    units=66
    """

    if "event" in request.form:
        return

    goal_type = request.form.get("type")
    commander_name = request.form.get("commander_identifier")
    qty = float(request.form.get("units"))

    user = Users.query.filter_by(commander_name=commander_name).first()

    commander_name = user.commander_name
    squad_id = user.squad_id

    contribution = Contributions.query.filter_by(
        squad_id=squad_id, user_id=user.id, units=goal_type
    ).first()

    if contribution is not None:
        # they have contributed before
        contribution.quantity = contribution.quantity + qty
    else:
        goal = Goals.query.filter_by(squad_id=squad_id, goal_units=goal_type).first()

        if goal is None:
            return jsonify({"response": "NOT_FOUND"})
        
        newContribution = Contributions(
            goal_id=goal.id,
            user_id=user.id,
            squad_id=squad_id,
            units=goal_type,
            quantity=qty
            )
        
        database.session.add(newContribution)

    database.session.commit()
    database.session.flush()

    return jsonify({"response": "OK"})
