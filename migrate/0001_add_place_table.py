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

CREATE TABLE place_mfw(
    id INT PRIMARY KEY,
    p_id INT NOT NULL,
    name VARCHAR(256) NOT NULL,
    hot INT,
    rating SMALLINT,
    level SMALLINT NOT NULL,
    location GEOGRAPHY(POINT,4326),
    tags VARCHAR[],
    created_at TIMESTAMP WITH TIME ZONE NOT NULL default NOW()
);


"""

# type: 0: unknown, 1:country, 2:city, 4:spot
# mfw level: in reference to PLACE_LEVEL

if __name__ == '__main__':
    conn = db.get_conn()
    db.execute_sql(conn,SQL)
    conn.commit()