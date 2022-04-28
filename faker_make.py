#! /usr/bin/env python
from contextlib import contextmanager

import faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import scoped_session

from sgu.models import Company, Employee

mysql_db = create_engine(
    "mysql+pymysql://root:123456789@127.0.0.1:3306/test?charset=utf8mb4", echo=True
)
Session = sessionmaker(bind=mysql_db)


@contextmanager
def scope_session():
    s = scoped_session(Session)
    try:
        yield s
    except Exception:
        s.rollback()
        s.remove()
        raise


def main():
    fake = faker.Faker()
    employee_cnt = 10000
    company_cnt = 1000
    for _ in range(company_cnt):
        with scope_session() as s:
            company = Company(name=fake.name())
            s.add(company)
            s.flush()
            company_id = company.id

        with scope_session() as s:
            employees = [
                Employee(name=fake.name(), company_id=company_id)
                for _ in range(employee_cnt)
            ]
            s.bulk_save_objects(employees)


if __name__ == "__main__":
    main()
