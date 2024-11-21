#!/usr/bin/env python3
""" End-to-end integration test for all the functionalities
    of the app.py and the endpoints using requests module
    """


import requests


URL = "http://localhost:5000{}"


def register_user(email: str, password: str) -> None:
    """ Test the app endpoint for regestring a new user
    """
    res = requests.post(
            URL.format("/users"),
            data={"email": email, "password": password})
    assert res.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
        Test the app endpoint login with a wrong password
        """
    res = requests.post(
            URL.format("/sessions"),
            data={"email": email, "password": password}
            )
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """
     Test the app endpoint to login a user with the correct email and password
     """
    res = requests.post(
             URL.format("/sessions"),
             data={"email": email, "password": password})
    assert res.json() == {"email": email, "message": "logged in"}
    session_id = res.cookies.get("session_id")
    assert session_id is not None
    return session_id


def profile_unlogged() -> None:
    """
        Test the app profile endpoint if the user is not logged in
        """
    res = requests.get(URL.format("/profile"))
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """
        Test the app profile when the user is logged in
        """
    cookies = dict(session_id=session_id)
    res = requests.get(URL.format("/profile"), cookies=cookies)
    assert res.status_code == 200


def log_out(session_id: str) -> None:
    """
        Test the app endpoint to destroy the user session
        """
    cookies = dict(session_id=session_id)
    res = requests.delete(
            URL.format("/sessions"),
            cookies=cookies,
            allow_redirects=False)
    assert res.status_code == 302


def reset_password_token(email: str) -> str:
    """
        Test the app endpoint that generates a token to reset the password
        """
    res = requests.post(URL.format("/reset_password"), data={"email": email})
    assert email in res.json().values()
    assert "reset_token" in res.json().keys()
    return res.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    res = requests.put(
            URL.format("/reset_password"),
            data={
                "email": email,
                "reset_token": reset_token,
                "new_password": new_password})
    assert res.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
