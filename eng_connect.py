import sqlalchemy as sa


def main():
    engine = sa.create_engine("sqlite:///engine.sqlite3", echo=True)
    with engine.connect() as c:
        c.execute(sa.text("""
        CREATE TABLE IF NOT EXISTS tb_parent (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(16) NOT NULL ,
            husband_id INTEGER references tb_child
        )
        """))
        c.execute(sa.text(f"""
        INSERT INTO tb_parent (name) VALUES (:name)
        """), [{"name": "xy"}, {"name": "xiaoxiao"}])
        
        rows = c.execute(sa.text("""
        SELECT * FROM tb_parent
        """))
        
        print(f"rows: {type(rows)} {rows}")
        result_iter = iter(rows)
        row = next(result_iter)
        print(f"row: {type(row)} => {row}")
        
        row_iter = iter(row)
        col = next(row_iter)
        print(f"col: {type(col)} => {col}")
        
        


if __name__ == '__main__':
    main()
