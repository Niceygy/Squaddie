from flask import redirect, render_template

from server.auth.capi import exchange_code_for_tokens, get_user_data
from server.constants import AUTHORIZATION_URL
from server.database.squad import get_squad_id
from server.database.tables import Users, database


def handle_authorize(request):
    return redirect(AUTHORIZATION_URL)

def handle_callback(request):
    try:
        code = request.args.get("code")
        expiry = request.args.get("expires_in")
        key, refresh_key = exchange_code_for_tokens(code)
        if key == "ERROR":
            return refresh_key
        else:
            commander_name, squad_name, squad_tag, token, refresh_token = get_user_data(
                key, refresh_key
            )
            
            return render_template(
                "public/auth/signup_after_capi.html",
                commander_name=commander_name,
                squad_name=squad_name,
            )
    except Exception as e:
        return e
    
def handle_create(request):
    password_hash = request.form.get("password_hash")
    commander_name = request.form.get("commander_name")
    squad_name = request.form.get("squad_name")
    
    newUser = Users(
        commander_name=commander_name,
        squad_id=get_squad_id(squad_name),
        password_hash=password_hash,
        progress_data={}
    )
    database.session.add(newUser)
    database.session.commit()

def handle_signup(request) -> str:
    return render_template("public/auth/signup_before_capi.html")
