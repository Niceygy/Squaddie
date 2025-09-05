from server.database.tables import Squads, database
from flask import render_template, request

def handle_squad_create(request) -> str:
    """
    GET and POST handler for /squads/create
    """
    commander_name = request.form.get("commander_name")
    squad_name = request.form.get("squad_name")
    squad_tag = request.form.get("squad_tag")
    rank = request.form.get("rank")

    if rank != "Owner":
        return render_template("public/auth/complete.html", commander_name=commander_name, message="Only commanders with rank 'Owner' can create a squad.")

    existing_squad = Squads.query.filter_by(sName=squad_name.lower()).first()
    if existing_squad:
        return render_template("public/auth/complete.html", commander_name=commander_name, message="Squad already exists.")

    new_squad = Squads(
        sName=squad_name.lower(),
        sTag=squad_tag,
        sOwner=commander_name,
        squad_word_hash=""
    )
    database.session.add(new_squad)
    database.session.commit()
    if not existing_squad and rank == "Owner":
        return render_template("public/auth/create_squad.html", commander_name=commander_name)
    return render_template("public/auth/complete.html", commander_name=commander_name, message="Squad created successfully!")