import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager

Base = declarative_base()


class Child(Base):
    __tablename__ = "tb_child"
    id = sa.Column("id", sa.Integer, primary_key=True)
    name = sa.Column("name", sa.String(16), nullable=False)
    age = sa.Column("age", sa.Integer, nullable=False)

    def __init__(self, name: str):
        self.name = name


class Parent(Base):
    __tablename__ = "tb_parent"
    def __init__(self, name: str):
        self.name = name

    id = sa.Column("id", sa.Integer, primary_key=True)
    name = sa.Column("name", sa.String(16), nullable=False)
    child_id = sa.Column("child_id", sa.ForeignKey(Child.id))



db = sa.create_engine("mysql+pymysql://root:123456789@127.0.0.1:3306/dev?charset=utf8mb4", echo=True)
Session = sessionmaker(bind=db)
s = Session()


def main():
    print("in main!")
    Base.metadata.create_all(db)

if __name__ == '__main__':
    main()
