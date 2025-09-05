from contextlib import contextmanager
import os
import traceback
from flask import Flask, make_response, redirect, render_template, request, g
from flask.cli import load_dotenv

from server.auth.handlers import handle_authorize, handle_callback, handle_create, handle_signin, handle_signup
from server.database.tables import database
from server.edmc import handle_cmdr_squad_lookup
from server.goals.update import handle_update
from server.squads.create import handle_squad_create
from server.squads.my_squad import handle_my_squad

"""
Init
"""

app = Flask(__name__)
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_POOL_SIZE"] = 10
app.config["SQLALCHEMY_POOL_TIMEOUT"] = 30
app.config["SQLALCHEMY_POOL_RECYCLE"] = 280
app.config["SQLALCHEMY_MAX_OVERFLOW"] = 20
database.init_app(app)

@contextmanager
def session_scope():
    session = database.session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        print(" * Closing session")
        session.close()

"""
Error Handlers
"""


@app.errorhandler(404)
def not_found(request):
    response = make_response(render_template("errors/404.html"), 404)
    return response


@app.errorhandler(Exception)
def internal_error(err):
    response = make_response(
        render_template("errors/500.html", info=str(err), stack=traceback.format_exc()),
        500,
    )
    return response

"""
Auth - cAPI
"""

@app.route("/auth/signup", methods=["GET"])
def signup():
    return handle_signup(request)

@app.route("/auth/authorize", methods=["GET"])
def authorize():
    return handle_authorize(request)

@app.route("/auth/callback", methods=["GET", "POST"])
def callback():
    return handle_callback(request)

@app.route("/auth/create", methods=["POST"])
def create_user():
    return handle_create(request)

@app.route("/auth/signin", methods=["GET", "POST"])
def auth_user():
    if g.is_authenticated:
        return redirect("/squads/me")
    else:
        return handle_signin(request)

@app.before_request
def check_auth_cookies():
    g.is_authenticated = False
    name = request.cookies.get("name")
    hash_val = request.cookies.get("hash")
    if name and hash_val:
        # Add your authentication logic here
        g.is_authenticated = True  # Set to True if cookies are valid

"""
Squad Pages
"""

@app.route("/squads/create", methods=["GET", "POST"])
def squad_create():
    return handle_squad_create(request)

@app.route("/squads/me", methods=["GET"])
def squad_homepage():
    return handle_my_squad(request)


"""
EDMC Plugin
"""

@app.route("/edmc/update", methods=["POST"])
def edmc_update():
    #plugin sends us data
    return handle_update(request)

@app.route("/edmc/search", methods=["POST"])
def edmc_search():
    #find the squad for a commander
    return handle_cmdr_squad_lookup(request)

"""
Public
"""

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555)
