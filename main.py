import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

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


def main():
    Base.metadata.create_all(db)


if __name__ == '__main__':
    main()
