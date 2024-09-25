#!/usr/bin/env python3
"""
    set up a basic Flask app.
    """


from flask import Flask, jsonify, request, abort
from auth import Auth

auth = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def index():
    """
        The main route
        """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """
        The endpoint to register a new user
        """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        new_user = auth.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": email, "message": "user created"})


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """
        Manage users sessions
        """
    email = request.form.get("email")
    password = request.form.get("password")

    # Validate the user's credentials
    if not auth.valid_login(email, password):
        abort(401)

    session_id = auth.create_session(email)
    res = jsonify({"email": email, "message": "logged in"})
    res.set_cookie("session_id", session_id)
    return res


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")