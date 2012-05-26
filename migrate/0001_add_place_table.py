from lib import db

SQL="""
CREATE TABLE place(
    id SERIAL PRIMARY KEY,
    name VARCHAR(256) NOT NULL,
    name_en VARCHAR(256) NOT NULL,
    slug VARCHAR(256) NOT NULL,
    type SMALLINT NOT NULL,
    parent_id INT,
    location GEOGRAPHY(POINT,4326),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL default NOW(),
);

CREATE UNIQUE INDEX place_slug_idx ON place(slug);
CREATE INDEX place_name_idx ON place(name);
CREATE INDEX place_location ON place USING GIST (location);
"""

# type: 0: unknown, 1:country, 2:city, 4:spot

if __name__ == '__main__':
    conn = db.get_conn()
    db.execute_sql(conn,SQL)
    conn.commit()