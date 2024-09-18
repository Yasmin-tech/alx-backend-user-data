#!/usr/bin/env python3
""" Main 5
"""
import uuid
from api.v1.auth.basic_auth import BasicAuth
from models.user import User

# """ Create a user test """
# user_email = str(uuid.uuid4())
user_email = "a45d9f21-bbaf-47bd-9492-c8cccd048ad9"
# user_clear_pwd = str(uuid.uuid4())
user_clear_pwd = "09e822fe93205472f7674a44abbe405d7073a59dcef4b33707fd7a525d33c6c0"
# user = User()
# user.email = user_email
# user.first_name = "Bob"
# user.last_name = "Dylan"
# user.password = user_clear_pwd
# print("New user: {}".format(user.display_name()))
# user.save()

""" Retreive this user via the class BasicAuth """

a = BasicAuth()

u = a.user_object_from_credentials(None, None)
print(u.display_name() if u is not None else "None")

u = a.user_object_from_credentials(89, 98)
print(u.display_name() if u is not None else "None")

u = a.user_object_from_credentials("email@notfound.com", "pwd")
print(u.display_name() if u is not None else "None")

u = a.user_object_from_credentials(user_email, "pwd")
print(u.display_name() if u is not None else "None")

u = a.user_object_from_credentials(user_email, user_clear_pwd)
print(u.display_name() if u is not None else "None")

