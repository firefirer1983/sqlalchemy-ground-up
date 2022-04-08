import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager

Base = declarative_base()

class RawMaterialEntry(Base):
    __tablename__ = "tb_raw_material_entry"
    id = sa.Column("id", primary_key=True)
    box_id = sa.Column("box_id", sa.ForeignKey("RawMaterialEntry.id"))
    entities = sa.relationship()

    
db = sa.create_engine("mysql+pymysql://root:123456789@127.0.0.1:3306/dev?charset=utf8mb4", echo=True)
Session = sessionmaker(bind=db)
s = Session()

def main():
    Base.metadata.create_all(db)

if __name__ == "__main__":
    main()

