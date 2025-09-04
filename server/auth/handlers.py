from flask import redirect

from server.auth.capi import exchange_code_for_tokens, get_user_data
from server.constants import AUTHORIZATION_URL


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
            cmdr_name, system_name, power, key, refresh_key = get_user_data(
                key, refresh_key
            )
            print("sucsess")
    except Exception as e:
        return e
