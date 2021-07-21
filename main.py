import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager

Base = declarative_base()


class Parent(Base):
    __tablename__ = "tb_parent"
    id = sa.Column("id", sa.Integer, primary_key=True)
    name = sa.Column("name", sa.String(16), nullable=False)


class Child(Base):
    __tablename__ = "tb_child"
    id = sa.Column("id", sa.Integer, primary_key=True)
    name = sa.Column("name", sa.String(16), nullable=False)


db = sa.create_engine("sqlite:///my.sqlite3?check_same_thread=False", echo=True)
Session = sessionmaker(bind=db)
ScopedSession = scoped_session(Session)


@contextmanager
def session_scoped(autocommit=False):
    s = Session()
    try:
        yield s
        if autocommit:
            s.commit()
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def main():
    Base.metadata.create_all(db)


if __name__ == '__main__':
    main()
