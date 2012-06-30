
def execute(conn, sql, params=()):
    cursor = conn.cursor()
    cursor.execute(sql, params)
