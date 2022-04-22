#! /usr/bin/env python
from __future__ import annotations

import sqlalchemy as sa
from typing import List
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, backref

Base = declarative_base()


class Parent(Base):
    __tablename__ = "tb_parent"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(16), nullable=False)

    children: List[Child] = relationship("Child", back_populates="parent", uselist=True)

    def __repr__(self) -> str:
        children_list = ",".join([f"{c.id}:{c.name} " for c in self.children])
        return f"{self.id}:{self.name}, parent of [ {children_list} ]"



class Child(Base):
    __tablename__ = "tb_child"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(16), nullable=False)
    parent_id = sa.Column(sa.Integer)

    parent: Parent = relationship(
        "Parent",
        foreign_keys=[parent_id],
        back_populates="children",
        primaryjoin="Parent.id==Child.parent_id",
    )

    def __repr__(self) -> str:
        return f"{self.id}:{self.name}, child of {self.parent.id}:{self.parent.name}"


db = sa.create_engine("sqlite:///rel_no_fk.sqlite3?check_same_thread=False", echo=True)
Session = sessionmaker(bind=db)
s = Session()


def main():
    p = Parent()
    p.children = [Child(), Child()]
    Base.metadata.create_all(db)


if __name__ == "__main__":
    main()
