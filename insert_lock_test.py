
import sqlalchemy as sa
import pymysql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
pymysql.install_as_MySQLdb()
Base = declarative_base()


class Box(Base):

    __tablename__ = "tb_box"

    id = sa.Column("id", sa.Integer, primary_key=True)
    serial_num = sa.Column("sn", sa.String(50), nullable=False)

    def __repr__(self) -> str:
        return f"Box(id:{self.id}, serial_num:{self.serial_num})"

    def __str__(self) -> str:
        return repr(self)

db = sa.create_engine("mysql://xy:123456789@127.0.0.1:3306/test?charset=utf8mb4", echo=True)
Session = sessionmaker(bind=db)
s = Session()

@contextmanager
def session_scope():
    s = Session()
    try:
        yield s
    except Exception as e:
        s.rollback()
        raise



def main():
    Base.metadata.create_all(db)
    box = s.query(Box).filter_by(id=3).with_for_update(nowait=True, read=True, of=Box).one()
    print(box)



if __name__ == "__main__":
    main()
