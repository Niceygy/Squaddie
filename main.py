from contextlib import contextmanager
import os
import traceback
from flask import Flask, make_response, render_template, request
from flask.cli import load_dotenv

from server.auth.handlers import handle_authorize, handle_callback
from server.database.tables import database

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

@app.route("/authorize", methods=["GET"])
def authorize():
    return handle_authorize(request)

@app.route("/callback", methods=["GET", "POST"])
def callback():
    return handle_callback(request)



"""
Public
"""

@app.route("/")
def index():
    return 'HELLO'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555)
