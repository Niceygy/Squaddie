from urllib.parse import quote_plus, urlencode
from server.constants import USER_AGENT, CAPI_TOKEN_URL, CODE_VERIFIER
import os
import requests

def make_request(url, token):
    headers = {"User-Agent": USER_AGENT, "Authorization": f"Bearer {token}"}
    API_URL = "https://companion.orerve.net/"
    resp = requests.get(f"{API_URL}{url}", headers=headers)
    return resp.json(), resp.status_code

def use_refresh_token(refresh_token: str) -> str:
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    client_id = os.getenv("CAPI_CLIENT_ID")
    client_secret = os.getenv("CAPI_CLIENT_SECRET")
    body = f"grant_type=refresh_token&client_id={client_id}&client_secret={client_secret}&refresh_token={refresh_token}"
    resp = requests.post(url=CAPI_TOKEN_URL, data=body, headers=headers)
    data = resp.json()
    return data

def exchange_code_for_tokens(code: str) -> list[str]:
    """Exchanges the auth code for a token

    Args:
        code (str): The auth codea

    Returns:
        list[str]: Access token, refresh token (if all OK), or
                   "ERROR" and the error text (if not OK)
    """
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": USER_AGENT,
    }
    data = urlencode(
        {
            "redirect_uri": os.getenv("CAPI_REDIRECT_URL"),
            "code": code,
            "grant_type": "authorization_code",
            "code_verifier": CODE_VERIFIER,
            "client_id": os.getenv("CAPI_CLIENT_ID"),
        }
    ).encode("utf-8")
    print(f"data = {data}")
    response = requests.post(CAPI_TOKEN_URL, headers=headers, data=data, timeout=50)
    if response.status_code == 200:
        tokens = response.json()
        ACCESS_TOKEN = tokens.get("access_token")
        REFRESH_TOKEN = tokens.get("refresh_token")
        # print(f"access token {ACCESS_TOKEN}")
        # print(f"refresh token {REFRESH_TOKEN}")
        return [ACCESS_TOKEN, REFRESH_TOKEN]
    else:
        print("Error exchanging code for tokens:", response.status_code, response.text)
        return ["ERROR", response.text]

def get_user_data(token, refresh_token) -> tuple[str, str, str, str, str]:
    """Gets the cAPI user data

    Args:
        token (str): cAPI token
        refresh_token (str): cAPI refresh token

    Returns: commander_name, squad_name, squad_tag, token, refresh_token
        
    """
    data, code = make_request("profile", token)
    if code != 200:
        #refresh
        data = use_refresh_token(refresh_token)
    else:
        commander_name =  data['commander']['name']
        squad_name = data['squadron']['name']
        squad_tag = data['squadron']['tag']
        return commander_name, squad_name, squad_tag, token, refresh_token
