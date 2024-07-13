from typing import Union, Optional, Sequence, Mapping

from django.db import connection, connections
from psycopg2.sql import Composed


DB_DEFAULT = "default"


def query_to_dicts(query: Union[str, Composed], input_params: Optional[Union[Sequence, Mapping]] = None, db_alias: str = DB_DEFAULT) -> list[dict]:
    conn = connections[db_alias] if db_alias != DB_DEFAULT else connection
    with conn.cursor() as c:
        query = c.mogrify(query, input_params) if db_alias != DB_DEFAULT else query
        c.execute(query)
        columns = [col[0] for col in c.description]
        rows = c.fetchall()
        return [dict(zip(columns, row)) for row in rows]
