#!/usr/bin/env python3
"""
    set up a basic Flask app.
    """


from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
