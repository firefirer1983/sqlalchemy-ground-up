from __future__ import annotations

from typing import List

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Employee(Base):
    __tablename__ = "tb_employee"
    id = Column(Integer, primary_key=True)
    name = Column(String(32), index=True, nullable=False)
    company_id = Column(Integer)
    company: Company = relationship(  # type: ignore
        "Company",
        foreign_keys=[company_id],
        primaryjoin="Employee.company_id==Company.id",
        back_populates="employees",
    )

    def __repr__(self) -> str:
        return f"Employee(id={self.id}, name={self.name} @<{self.company.name}>)"


class Company(Base):
    __tablename__ = "tb_company"
    id = Column(Integer, primary_key=True)
    name = Column(String(32), index=True, nullable=False)
    employees: List[Employee] = relationship(  # type: ignore
        "Employee",
        uselist=True,
        foreign_keys="Employee.company_id",
        primaryjoin="Employee.company_id==Company.id",
        back_populates="company",
    )

    def __repr__(self) -> str:
        return f"Compay(id={self.id}, name={self.name}, \
        employees={[emp for emp in self.employees]})"


class Parenting(Base):
    __tablename__ = "tb_child_parent"
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, index=True)
    child_id = Column(Integer, index=True)


class Child(Base):
    __tablename__ = "tb_child"
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    parents: List[Parent] = relationship(  # type: ignore
        "Parent",
        uselist=True,
        secondary="tb_child_parent",
        primaryjoin="Child.id==Parenting.child_id",
        secondaryjoin="Parenting.parent_id==Parent.id",
        back_populates="children",
    )

    def __repr__(self) -> str:
        return f"Child(id={self.id}, name={self.name}, \
        parents={[p.name for p in self.parents]})"


class Parent(Base):
    __tablename__ = "tb_parent"
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    children: List[Child] = relationship(  # type: ignore
        "Child",
        uselist=True,
        secondary="tb_child_parent",
        primaryjoin="Parent.id==Parenting.parent_id",
        secondaryjoin="Parenting.child_id==Child.id",
        back_populates="parents",
    )

    def __repr__(self) -> str:
        return f"Parent(id={self.id}, name={self.name}, \
        children={[c.name for c in self.children]})"


class Wife(Base):
    __tablename__ = "tb_wife"
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    husband_id = Column(Integer)
    husband = relationship(
        "Husband",
        uselist=False,
        foreign_keys=[husband_id],
        primaryjoin="Wife.husband_id==Husband.id",
        back_populates="wife",
    )


class Husband(Base):
    __tablename__ = "tb_husband"
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    wife = relationship(
        "Wife",
        uselist=False,
        foreign_keys="Wife.husband_id",
        primaryjoin="Wife.husband_id==Husband.id",
        back_populates="husband",
    )
