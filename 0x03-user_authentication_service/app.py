#!/usr/bin/env python3
"""
    set up a basic Flask app.
    """


from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth

AUTH = Auth()
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
        new_user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": email, "message": "user created"})


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """POST /sessions
    Return:
        - The account login payload.
    """
    email, password = request.form.get("email"), request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """
        The endpoint to logout a user
        """
    # Get the session_id from the cookie that is set in the login route
    session_id = request.cookies.get("session_id")

    # if the user does not exist, return a 403 status
    user_instance = AUTH.get_user_from_session_id(session_id)
    if user_instance is None:
        abort(403)

    # if the user exists, destroy the session_id and redirect to the main page
    AUTH.destroy_session(user_instance.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """
        The endpoint to get the profile of a user
        """

    # if the session_id is not set, return a 403 status
    session_id = request.cookies.get("session_id")
    if session_id is None:
        abort(403)

    # if the user does not exist, return a 403 status
    user_instance = AUTH.get_user_from_session_id(session_id)
    if user_instance is None:
        abort(403)

    # if the user exists, return the profile information
    return jsonify({"email": user_instance.email}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """
        Get a reset_password_token if user with the given email exists
        """
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": reset_token}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
