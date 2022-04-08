#! /usr/bin/env python

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from contextlib import contextmanager

Base = declarative_base()


class Parent(Base):
    __tablename__ = "tb_parent"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(16), nullable=False)

    def __repr__(self) -> str:
        children_list = ",".join([f"{c.id}:{c.name} " for c in self.children])
        return f"{self.id}:{self.name}, parent of [ {children_list} ]"


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

    def __repr__(self) -> str:
        return f"{self.id}:{self.name}, child of {self.parent.id}:{self.parent.name}"


db = sa.create_engine("sqlite:///rel_no_fk.sqlite3?check_same_thread=False", echo=True)
Session = sessionmaker(bind=db)
s = Session()


def main():
    Base.metadata.create_all(db)


if __name__ == "__main__":
    main()
