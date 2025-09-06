import base64
import hashlib
import os
from urllib.parse import quote_plus

"""
Session Spesific Keys
"""

CODE_VERIFIER = base64.urlsafe_b64encode(os.urandom(32)).decode("utf-8")
CODE_CHALLENGE = base64.urlsafe_b64encode(hashlib.sha256(CODE_VERIFIER.encode()).digest()).decode("utf-8").rstrip("=")
SESSION_STATE = base64.urlsafe_b64encode(os.urandom(32)).decode("utf-8").rstrip("=")

_URI = os.getenv("CAPI_REDIRECT_URL")
print(_URI)
_REDIRECT_URI = quote_plus(_URI)
_CLIENT_ID = os.getenv("CAPI_CLIENT_ID")

AUTHORIZATION_URL = (
    "https://auth.frontierstore.net/"
    "auth?response_type=code&"
    "approval_prompt=auto&"
    f"client_id={_CLIENT_ID}&"
    f"redirect_uri={_REDIRECT_URI}&"
    f"state={SESSION_STATE}&"
    f"code_challenge={CODE_CHALLENGE}&"
    "code_challenge_method=S256&"
    "scope=auth%20capi"
    )

"""

"""

USER_AGENT = "EDCD-Squaddie-0.0.1"
CAPI_TOKEN_URL = os.getenv("CAPI_BASE_URL") + "/token"

GOAL_TYPES = {
    "Combat Bonds": "combat",
    "Trade": "trade profits",
}