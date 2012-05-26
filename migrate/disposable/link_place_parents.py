# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals, print_function
import os
import sys
import csv
sys.path.append(os.path.abspath('..'))
from lib import db

if __name__ == '__main__':
    conn = db.get_conn()
    with open('/Users/nanfang/places.csv', 'r') as f:
        r = csv.reader(f)
        header = True
        for name,name_en,slug,parent_slug,type,latitude,longitude in r:
            db.execute_sql(conn, 'UPDATE place set parent_id=(SELECT id FROM place WHERE slug=%s) where slug=%s', (parent_slug,slug))
    conn.commit()
    print('done')


