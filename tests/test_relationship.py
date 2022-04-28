import allure

from sgu.models import Child, Company, Employee, Husband, Parent, Wife


@allure.feature("ORM关系对象管理")
class TestRelationship:
    @allure.story("创建关系: 一对一")
    def test_1(self, session, faker):
        wife = Wife(name=faker.name())
        wife.husband = Husband(name=faker.name())
        session.add(wife)
        session.commit()
        assert (
            session.query(Wife)
            .filter(Wife.husband.has(Husband.id == wife.husband.id))
            .one()
            == wife
        )

    @allure.story("创建关系: 一对多")
    def test_2(self, session, faker):
        EMPLOYEE_COUNT = 100
        company = Company(name=faker.name())
        company.employees = [Employee(name=faker.name()) for _ in range(EMPLOYEE_COUNT)]
        session.add(company)
        session.commit()

        assert (
            session.query(Employee).filter(Employee.company_id == company.id).count()
            == EMPLOYEE_COUNT
        )

    @allure.story("创建关系: 多对多")
    def test_3(self, session, faker):
        CHILD_COUNT = 3
        mother, father = Parent(name=faker.name()), Parent(name=faker.name())
        mother.children = [Child(name=faker.name()) for _ in range(CHILD_COUNT)]
        father.children = mother.children
        session.add_all([mother, father])
        session.commit()
        mother2: Parent = session.query(Parent).filter_by(id=mother.id).one()
        father2: Parent = session.query(Parent).filter_by(id=father.id).one()
        assert len(mother2.children) == CHILD_COUNT
        assert len(father2.children) == CHILD_COUNT
        assert mother2.children == father2.children
