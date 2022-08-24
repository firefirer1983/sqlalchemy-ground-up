import os
import sys

import pytest
from sqlalchemy import create_engine, event
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
    Base.metadata.create_all(db)
    yield
    if db != mysql_db:
        Base.metadata.drop_all(db)


@pytest.fixture(autouse=True)
def env(schema):
    s = scoped_session(Session)
    company = Company(name="ikasinfo")
    company.employees = [Employee(name="xy"), Employee(name="djm")]
    s.add(company)
    children = [Child(name="jerry"), Child(name="darling")]
    parents = [Parent(name="xy"), Parent(name="xiao")]
    for parent in parents:
        parent.children = children
    s.add_all(parents)
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


@pytest.fixture()
def nested():
    s = scoped_session(Session)
    s.begin_nested()
    yield s

    @event.listens_for(s, "after_transaction_end")
    def restart_savepoint(s, t):
        if t.nested and (t._parent is not None and not t._parent.nested):
            s.expire_all()
            s.begin_nested()

    event.remove(s, "after_transaction_end", restart_savepoint)


@pytest.fixture(scope="session")
def faker():
    from faker import Faker

    return Faker()
