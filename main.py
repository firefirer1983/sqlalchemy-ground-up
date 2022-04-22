from contextlib import contextmanager

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()


class Parent(Base):
    __tablename__ = "tb_parent"
    id = sa.Column("id", sa.Integer, primary_key=True)
    name = sa.Column("name", sa.String(16), nullable=False)
    child_id = sa.Column("child_id", sa.Integer)
    @property
    def age(self) -> str:
        return str(10)

    @age.setter
    def age(self, val):
        print(f"set age to {val}")



class Child(Base):
    __tablename__ = "tb_child"
    id = sa.Column("id", sa.Integer, primary_key=True)
    name = sa.Column("name", sa.String(16), nullable=False)
    parent_id = sa.Column("parent_id", sa.Integer)


db = sa.create_engine("sqlite:///my.sqlite3?check_same_thread=False", echo=True)
Session = sessionmaker(bind=db)
ScopedSession = scoped_session(Session)


@contextmanager
def scope_session():
    s = Session()
    try:
        yield s
    except Exception:
        s.rollback()
        raise
    finally:
        s.close()


def main():
    Base.metadata.create_all(db)


if __name__ == "__main__":
    main()
