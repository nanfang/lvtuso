# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals, print_function
import os
import sys
import csv

sys.path.append(os.path.abspath('..'))
from lib import db


# type: 0: unknown, 1:country, 2:city, 4:spot
types = dict(
    unknown=0,
    country=1,
    city=2,
    spot=4,
)

if __name__ == '__main__':
    conn = db.get_conn()
    with open('/Users/nanfang/places.csv', 'r') as f:
        r = csv.reader(f)
        header = True
        for name,name_en,slug,parent_slug,type,latitude,longitude in r:
            name = unicode(name,"utf-8")
            name_en = unicode(name_en,"utf-8")
            if header:
                header = False
                continue
            if latitude and longitude:
                db.execute_sql(conn,"""
                    INSERT INTO place(name,name_en,slug,type,location) values
                    (%%s,%%s,%%s,%%s,ST_GeomFromText('POINT(%s %s)', 4326))
                    """ % (longitude, latitude)
                    , (name,name_en,slug,types.get(type,0))
                )

            else:
                db.execute_sql(conn,'INSERT INTO place(name,name_en,slug,type) values (%s,%s,%s,%s)',
                    (name,name_en,slug,types.get(type,0))
                )
            print('imported %s' % name)

    conn.commit()


