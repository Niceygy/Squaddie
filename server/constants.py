import base64
import hashlib
import os
from urllib.parse import quote_plus

"""
Session Spesific Keys
"""

CODE_VERIFIER = base64.urlsafe_b64encode(os.urandom(32)).decode("utf-8")
"""
Session spesific code verifier for cApi logon. Base64
"""
CODE_CHALLENGE = base64.urlsafe_b64encode(hashlib.sha256(CODE_VERIFIER.encode()).digest()).decode("utf-8").rstrip("=")
"""
Session spesific code challenge for cApi logon. Base64
"""
SESSION_STATE = base64.urlsafe_b64encode(os.urandom(32)).decode("utf-8").rstrip("=")
"""
Session spesific session state for cApi logon. Base64
"""

_URI = os.getenv("CAPI_REDIRECT_URL")
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
Capi logon URI
"""

"""
Constant... Constants
"""

USER_AGENT = "EDCD-Squaddie-0.0.1"
"""User agent for Capi and plugin requests"""
CAPI_TOKEN_URL = os.getenv("CAPI_BASE_URL") + "/token"

GOAL_TYPES = [
    "Combat Bonds",
    "Trade",
    "Exploration",
    "Powerplay",
    "Exobiology"
]
"""
Accepted goal types
"""

GOAL_UNITS = {
    "Combat Bonds": "CR",
    "Trade": "CR",
    "Exploration": "CR",
    "Powerplay": "MERITS",
    "Exobiology": "CR"
}
"""
What you need to earn for each of the goal types
"""

GOAL_MESSAGES = {
    "Combat Bonds": "EARN COMBAT BONDS",
    "Trade": "TRADE FOR PROFTS",
    "Exploration": "SELL EXPLORATION DATA",
    "Powerplay": "EARN POWERPLAY MERITS",
    "Exobiology": "SELL BIO DATA"
}
"""
Basic instructions for each of the goal types
"""

GOAL_MESSAGE_TEMPLATE = "THIS GOAL REQUIRES YOU TO"
GOAL_PLUGIN_LINKED = "YOUR EDMC SQUADDIE PLUGIN IS WORKING & CONNECTED!"
GOAL_PLUGIN_NOTLINKED = "SQUADDIE CANNOT SEE THAT YOUR EDMC PLUGIN IS WORKING! USE IT TO TRACK YOUR PROGRESS. DOWNLOAD HERE"
GOAL_PLUGIN_URL = "https://github.com/niceygy/squaddieedmc/releases/latest"