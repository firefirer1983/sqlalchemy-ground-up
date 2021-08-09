import sqlalchemy as sa
import pytest as pt
import sys
import os

TEST_BASE_PATH = os.path.dirname(os.path.dirname(__file__))
sys.path.append(TEST_BASE_PATH)

from tests.configure import Config


@pt.fixture(scope="module")
def test_connect():
    
    db_ = sa.create_engine("sqlite:///tmp.sqlite3", echo=True)
    with db_.connect() as c:
        c.execute(sa.text("""
        CREATE TABLE IF NOT EXISTS tb_parent (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(16) NOT NULL ,
            child_id INTEGER references tb_children
        )
        """))
        c.execute(sa.text("""
        CREATE TABLE IF NOT EXISTS tb_children (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(16) NOT NULL ,
            parent_id INTEGER references tb_parent
        )
        """))
        c.execute(
            sa.text("""
                INSERT INTO tb_parent (name) VALUES (:name)
            """),
            [{"name": "xy"}, {"name": "xiaoxiao"}]
        )
        c.execute(
            sa.text("""
                INSERT INTO tb_children (name) VALUES (:name)
            """),
            [{"name": "ruiheng"}, {"name": "ryon"}]
        )
        yield c
        # c.execute(sa.text("""
        #     DROP TABLE tb_parent;
        # """))
        # c.execute(sa.text("""
        #     DROP TABLE tb_children;
        # """))
