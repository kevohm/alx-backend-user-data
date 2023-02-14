#!/usr/bin/env python3
"""
Auth module
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
import uuid
from user import User


def _hash_password(password: str) -> str:
    """Hash a password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """generate uuid
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register users
        """
        hashed = _hash_password(password)
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(user.email))
        except NoResultFound:
            return self._db.add_user(email=email, hashed_password=hashed)

    def valid_login(self, email: str, password: str) -> bool:
        """check if login is valid
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """creates a session_id
        """
        try:
            user = self._db.find_user_by(email=email)
            uid = _generate_uuid()
            self._db.update_user(user.id, session_id=uid)
            return uid
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """get user by session_id
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """removes users session_id
        """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """create reset token
        """
        try:
            user = self._db.find_user_by(email=email)
            uid = _generate_uuid()
            self._db.update_user(user.id, reset_token=uid)
        except NoResultFound:
            raise ValueError
