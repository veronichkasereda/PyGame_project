import datetime

import sqlalchemy
from flask_login import UserMixin

from db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True,
                           nullable=False)
    team_leader = sqlalchemy.Column(sqlalchemy.String,
                                    nullable=True)
    job = sqlalchemy.Column(sqlalchemy.String,
                            nullable=True)
    work_size = sqlalchemy.Column(sqlalchemy.Integer)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                   default=datetime.datetime.now())
    is_finished = sqlalchemy.Column(sqlalchemy.BOOLEAN)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime)

    def __repr__(self):
        return f'<Colonist> {self.id} {self.name} {self.surname}'
