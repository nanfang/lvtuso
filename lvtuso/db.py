import psycopg2
from lvtuso.settings import DB

def get_conn():
    return psycopg2.connect(
        host=DB['HOST'],
        port=DB['PORT'],
        user=DB['USER'],
        password=DB['PASSWORD'],
        database=DB['NAME'])


def execute_sql(conn, sql, params=()):
    cursor = conn.cursor()
    cursor.execute(sql, params)
