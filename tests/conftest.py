import os
import sys

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import scoped_session

from sgu.models import Base, Child, Company, Employee, Husband, Parent, Wife

TEST_BASE_PATH = os.path.dirname(os.path.dirname(__file__))
sys.path.append(TEST_BASE_PATH)

memory_db = create_engine("sqlite://", echo=True)
local_db = create_engine("sqlite:///test.sqlite3?check_same_thread=False", echo=True)
mysql_db = create_engine(
    "mysql+pymysql://root:123456789@127.0.0.1:3306/test?charset=utf8mb4", echo=True
)
db = memory_db
Session = sessionmaker(bind=memory_db)


@pytest.fixture()
def schema():
    if db == mysql_db:
        return
    Base.metadata.create_all(db)
    yield
    Base.metadata.drop_all(db)


@pytest.fixture(autouse=True)
def env(schema):
    s = scoped_session(Session)
    company = Company(name="ikasinfo")
    company.employees = [Employee(name="xy"), Employee(name="djm")]
    s.add(company)
    child = Child(name="jerry")
    child.parents = [Parent(name="xy"), Parent(name="xiao")]
    s.add(child)
    wife = Wife(name="xiao")
    wife.husband = Husband(name="xy")
    s.commit()


@pytest.fixture()
def session():
    s = scoped_session(Session)
    try:
        yield s
    except Exception:
        s.rollback()
        s.remove()
        raise


@pytest.fixture(scope="session")
def faker():
    from faker import Faker

    return Faker()
