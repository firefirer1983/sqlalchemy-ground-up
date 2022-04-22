from contextlib import contextmanager

import pymysql
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

pymysql.install_as_MySQLdb()
Base = declarative_base()


class Box(Base):

    __tablename__ = "tb_box"

    id = sa.Column("id", sa.Integer, primary_key=True)
    serial_num = sa.Column("sn", sa.String(50), nullable=False)


db = sa.create_engine(
    "mysql://xy:123456789@127.0.0.1:3306/test?charset=utf8mb4", echo=True
)
Session = sessionmaker(bind=db)
ScopedSession = scoped_session(Session)


@contextmanager
def session_scoped():
    s = Session()
    try:
        yield s
    except Exception as e:
        s.rollback()
        raise e


s = Session()


def main():
    Base.metadata.create_all(db)


if __name__ == "__main__":
    main()
