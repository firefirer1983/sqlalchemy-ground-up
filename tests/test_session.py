import allure
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import scoped_session


@allure.feature("Session管理")
class TestRelationship:
    @allure.story("线程local session")
    def test_1(self):
        db = create_engine("sqlite://", echo=True)
        Session = sessionmaker(bind=db)
        assert Session(bind=db) != Session(bind=db)
        assert scoped_session(Session) is scoped_session(Session)
