import sqlalchemy as sa
from sqlalchemy.orm import relationship
from . import db, Base


# one-to-one: 夫妻关系,是一对一的关系,丈夫只有一个妻子,妻子只有一个丈夫

class Man(Base):
    __tablename__ = "tb_man"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(16), nullable=False)
    wife = relationship("Woman", backref="husband", uselist=False)


class Woman(Base):
    __tablename__ = "tb_woman"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(16), nullable=False)
    husband_id = sa.Column(sa.Integer, sa.ForeignKey("tb_man.id"))


# one-to-many: 雇佣关系,是一对多的关系,雇主有多个雇员,雇员只有一个雇主
class Employer(Base):
    __tablename__ = "tb_employer"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(16), nullable=False)
    employee = relationship("Employee", backref="employer")


class Employee(Base):
    __tablename__ = "tb_employee"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(16), nullable=False)
    boss_id = sa.Column(sa.Integer, sa.ForeignKey("tb_employer.id"))


# many-to-many: 订阅关系,是多对多的关系,一个用户有多个订阅的频道,一个频道有多个订阅者
class SubscribeRelation(Base):
    __tablename__ = "tb_subscribe_relation"
    user_id = sa.Column(
        sa.Integer, sa.ForeignKey('tb_user.id'), primary_key=True
    ),
    channel_id = sa.Column(
        sa.Integer, sa.ForeignKey('tb_channel.id'), primary_key=True
    )


class User(Base):
    __tablename__ = "tb_user"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(16), nullable=False)
    subscriptions = relationship(
        "Channel", secondary=SubscribeRelation, backref="subscribers",
        lazy="dynamic"
    )


class Channel(Base):
    __tablename__ = "tb_channel"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(16), nullable=False)


if __name__ == '__main__':
    Base.metadata.create_all(db)
