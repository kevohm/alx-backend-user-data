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
