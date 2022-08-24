import allure

from sgu.models import Child, Company, Employee, Parent


@allure.feature("exist子查询")
class TestRelationship:
    @allure.story("多对一has(Employee.comany.has)")
    def test_1(self, session, faker):
        """

        SELECT *
        FROM tb_employee
        WHERE EXISTS (SELECT 1
        FROM tb_company
        WHERE tb_employee.company_id = tb_company.id AND tb_company.name = 'ikasinfo')

        """
        EMPLOYEE_COUNT = 100
        company = Company(name=faker.name())
        company.employees = [Employee(name=faker.name()) for _ in range(EMPLOYEE_COUNT)]
        session.add(company)
        session.commit()
        stmt = session.query(Employee).filter(
            Employee.company.has(Company.name == company.name)
        )
        cnt = stmt.count()
        assert cnt == EMPLOYEE_COUNT

    @allure.story("一对多用any(Company.employees.any)")
    def test_2(self, session, faker):
        """

        SELECT *
        FROM tb_company
        WHERE EXISTS (SELECT 1
        FROM tb_employee
        WHERE tb_employee.company_id = tb_company.id AND tb_employee.name='xxx'

        """

        EMPLOYEE_COUNT = 3
        company = Company(name=faker.name())
        company.employees = [Employee(name=faker.name()) for _ in range(EMPLOYEE_COUNT)]
        session.add(company)
        session.commit()
        stmt = session.query(Company).filter(
            Company.employees.any(Employee.name == company.employees[0].name)
        )
        assert len(stmt.first().employees) == EMPLOYEE_COUNT

    @allure.story("多对多用any")
    def test_3(self, session, faker):
        """

        SELECT *
        FROM tb_child
        WHERE EXISTS (SELECT 1
        FROM tb_child_parent, tb_parent
        WHERE tb_child.id = tb_child_parent.child_id
        AND tb_child_parent.parent_id = tb_parent.id
        AND tb_parent.id IN (1,2))'

        """
        CHILD_COUNT = 10
        children = [Child(name=faker.name()) for _ in range(CHILD_COUNT)]
        parents = [Parent(name=faker.name()) for _ in range(2)]
        for parent in parents:
            parent.children = children
            session.add(parent)
        session.add_all(parents)
        session.commit()
        stmt = session.query(Child).filter(
            Child.parents.any(Parent.id.in_([p.id for p in parents]))
        )
        for child in stmt.all():
            for parent in parents:
                assert parent in child.parents
