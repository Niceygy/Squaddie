import traceback
from flask import Flask, make_response, render_template, request
from flask.cli import load_dotenv

from server.auth.auth import handle_authorize, handle_callback

app = Flask(__name__)
load_dotenv()

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
