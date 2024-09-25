#!/usr/bin/env python3
"""DB modle
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
# from sqlalchemy.exc import NoResultFound

from user import Base
from user import User
from typing import Dict


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
            create a new user instance and save the user to the database
            """
        user_obj = User(email=email, hashed_password=hashed_password)
        self._session.add(user_obj)
        self._session.commit()
        return user_obj

    def find_user_by(self, **kwargs: Dict) -> User:
        """
            This method takes in arbitrary keyword arguments and
            returns the first row found in the users table as filtered by
            the method’s input arguments
            """
        user_obj = self._session.query(User).filter_by(**kwargs).one()
        # if user_obj is None:
        #     raise NoResultFound
        return user_obj

    def update_user(self, user_id: int, **kwargs: Dict) -> None:
        """
            Update the user that has user_id and commit the changes
            - if user is not found, nothing is changed and no error is raised
            - if arguments in kwargs that does not correspond to a user
                attribute is passed, raise a ValueError
            """
        # try:
        #     user_obj = self.find_user_by(id=user_id)
        # except NoResultFound:
        #     return
        user_obj = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user_obj, key):
                raise ValueError
            setattr(user_obj, key, value)
        self._session.commit()
