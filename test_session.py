from typing import Any

import sqlalchemy

from main import ScopedSession, Session


def test_simple_session():
    s1 = Session()
    s2 = Session()
    assert s1 is not s2  # Session() 每次都是不同的 sqlalchemy.orm.Session 对象
    assert isinstance(s1, sqlalchemy.orm.Session)
    assert isinstance(s2, sqlalchemy.orm.Session)


def test_scoped_session():
    # scoped_session每次都是同一个Session对象
    s1 = ScopedSession()
    s2 = ScopedSession()
    assert s1 is s2
    assert isinstance(s1, sqlalchemy.orm.Session)
    assert isinstance(s2, sqlalchemy.orm.Session)


def test_thread_local():
    def assert_unique(a: Any, b: Any):
        assert a is not b

    def assert_not_unique(a: Any, b: Any):
        assert a is b

    import threading

    s1 = ScopedSession()
    t = threading.Thread(
        target=lambda s: assert_unique(s, ScopedSession())
        and assert_not_unique(ScopedSession(), ScopedSession()),
        args=(s1,),
    )
    t.start()
    t.join()
