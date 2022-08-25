#! /usr/bin/env python
from __future__ import annotations
from typing import List
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

# tb_parent_child = sa.Table(
#     "tb_parent_child",
#     Base.metadata,
#     sa.Column("parent_id", sa.Integer, primary_key=True),
#     sa.Column("child_id", sa.Integer, primary_key=True),
# )

class ParentChild(Base):
    __tablename__ = "tb_parent_child"
    # id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    parent_id = sa.Column(sa.Integer, primary_key=True)
    child_id = sa.Column(sa.Integer, primary_key=True)


class Parent(Base):
    __tablename__ = "tb_parent"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(16), nullable=False)
    is_vip = sa.Column(sa.Boolean, default=False)

    def __init__(self, name: str) -> None:
        super().__init__(name=name)

    children: List[Child] = relationship(
        "Child",
        secondary="tb_parent_child",
        back_populates="parents",
        primaryjoin="ParentChild.parent_id==Parent.id",
        secondaryjoin="ParentChild.child_id==Child.id"
    )

    def __repr__(self) -> str:
        children_list = ",".join([f"{c.id}:{c.name} " for c in self.children])
        return f"{self.id}:{self.name}, parent of {children_list}"


class Child(Base):
    __tablename__ = "tb_child"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    def __init__(self, name: str) -> None:
        super().__init__(name=name)

    name = sa.Column(sa.String(16), nullable=False)

    parents: List[Parent] = relationship(
        "Parent",
        secondary="tb_parent_child",
        back_populates="children",
        primaryjoin=("Child.id==ParentChild.child_id"),
        secondaryjoin=("ParentChild.parent_id==Parent.id")
    )

    def __repr__(self) -> str:
        parents_list = ",".join([f"{p.id}:{p.name}" for p in self.parents])
        return f"{self.id}:{self.name}, child of {parents_list}"


db = sa.create_engine("sqlite://", echo=True)
Session = sessionmaker(bind=db)
s = Session()


def main():
    Base.metadata.create_all(db)
    h = Parent("xy")
    w = Parent("xx")
    h.children = w.children = [Child("ray"), Child("darlin")]
    s.add(h)
    s.commit()
    xy, xx = s.query(Parent).all()
    print(xy)
    print(xx)


if __name__ == "__main__":
    main()
