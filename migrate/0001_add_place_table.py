from lib import db

SQL="""
CREATE TABLE place(
    id SERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    type SMALLINT NOT NULL
);
"""

if __name__ == '__main__':
    conn = db.get_conn()
    db.execute_sql(conn,SQL)
    conn.commit()