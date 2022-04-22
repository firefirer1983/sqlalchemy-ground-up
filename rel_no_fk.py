#! /usr/bin/env python


import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Parent(Base):
    __tablename__ = "tb_parent"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(16), nullable=False)


class Child(Base):
    __tablename__ = "tb_child"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(16), nullable=False)
    parent_id = sa.Column(sa.Integer)
    parent = relationship(
        Parent,
        backref="children",
        foreign_keys=[parent_id],
        primaryjoin="Parent.id==Child.parent_id",
    )


db = sa.create_engine("sqlite:///rel_no_fk.sqlite3?check_same_thread=False", echo=True)
Session = sessionmaker(bind=db)
s = Session()


def main():
    Base.metadata.create_all(db)


if __name__ == "__main__":
    main()
