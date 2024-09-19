#!/usr/bin/env python3
"""
    This model contains the route to log in a user and
    set the a cookie with the session id
    """


from api.v1.views import app_views
from flask import make_response, jsonify, request
from models.user import User
from os import getenv


@app_views.route("/auth_session/login", methods=['POST'], strict_slashes=False)
def log_in():
    """ - check the credentials of the user
        - set the session cookies
        - return a dictionary representation of the User
        """
    email = request.form.get("email")
    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get("password")
    if not password:
        return jsonify({"error": "password missing"}), 400

    # User.load_from_file()
    user_list = User.search({"email": email})

    if not user_list or len(user_list) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user_found = user_list[0]
    if not user_found.is_valid_password(password):
        jsonify({"error": "wrong password"}), 401

    # a user is found with the correct password
    from api.v1.app import auth
    session_id = auth.create_session(user_found.id)
    rsp = jsonify(user_found.to_json())
    rsp.set_cookie(getenv("SESSION_NAME"), session_id)
    return rsp
