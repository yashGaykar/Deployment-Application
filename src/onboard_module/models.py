from sqlalchemy import Column, String, Integer, UniqueConstraint, ForeignKey, Boolean

from ..db import db


class AWSAccount(db.Model):
    """Model for AWS ACCOUNTS table"""

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_name = Column(String(50), unique=True)
    access_key = Column(String(100))
    secret_key = Column(String(100))
    key_name = Column(String(50), unique=True)
    active_status = Column(Boolean, default=True, unique=False)
