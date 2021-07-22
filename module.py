from sgu import db, Session, ScopedSession, session_scoped, Base
from sgu.models import Man, Woman #, Employee, Employer, Channel, User

if __name__ == '__main__':
    Base.metadata.create_all(bind=db)
