import datetime

import sqlalchemy

from db_session import SqlAlchemyBase
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True,
                           nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String,
                             nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String,
                                nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer,
                            nullable=True)
    position = sqlalchemy.Column(sqlalchemy.String)
    speciality = sqlalchemy.Column(sqlalchemy.String)
    address = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String,
                              unique=True,
                              index=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now())


def check_password(self, passw):
    return self.hashed_pasword == passw