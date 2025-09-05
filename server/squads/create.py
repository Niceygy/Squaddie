from server.database.tables import Squads, database
from flask import render_template, request

def handle_squad_create(request) -> str:
    """
    GET and POST handler for /squads/create
    """
    if request.method == "GET":
        return render_template(
            "squad/create_squad.html",
            commander_name=request.cookies.get("name"),
            squad_name=request.cookies.get("squad_name"),
            squad_tag=request.cookies.get("squad_tag")
            )
    else:
        commander_name = request.form.get("commander_name")
        squad_name = request.form.get("squad_name")
        squad_tag = request.form.get("squad_tag")
        rank = request.form.get("rank")

        if rank != "Owner" and False: #TEMP
            return render_template("errors/generic.html", commander_name=commander_name, error_title="You can't do this!", error_message="Only commanders with rank 'Owner' can create a squad.")

        if squad_name is not None:
            existing_squad = Squads.query.filter_by(sName=squad_name.lower()).first()
            if existing_squad:
                return render_template("squad/complete.html", squad_name=squad_name, message="Squad already exists.")

        new_squad = Squads(
            sName=squad_name.lower(),
            sTag=squad_tag,
            sOwner=commander_name,
            squad_word_hash=""
        )
        database.session.add(new_squad)
        database.session.commit()
    # if not existing_squad and rank == "Owner":
    #     return render_template("auth/create_squad.html", commander_name=commander_name)
        return render_template("squad/complete.html", commander_name=commander_name, message="Squad created successfully!")