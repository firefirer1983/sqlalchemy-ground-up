import os
from contextlib import contextmanager

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

Base = declarative_base()

db = sqlalchemy.create_engine(
    f"sqlite:////{BASE_DIR}/my.sqlite3?check_same_thread=False", echo=True
)
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
