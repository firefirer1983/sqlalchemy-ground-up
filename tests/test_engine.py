from sqlalchemy import text
from sqlalchemy.engine.base import Connection
from sqlalchemy.engine.result import ResultProxy, RowProxy


def test_result_proxy(test_connect: Connection):
    result = test_connect.execute(
        text(
            """
    SELECT * FROM tb_parent
    """
        )
    )
    assert type(result) == ResultProxy

    rows = iter(result)
    row = next(rows)
    assert type(row) == RowProxy

    cols = iter(row)
    assert hasattr(row, "id")
    assert type(row["id"]) == int
    row["name"] = "fyman"
    col = next(cols)
    assert type(col) is int
