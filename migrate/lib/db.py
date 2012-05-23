# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals, print_function
import psycopg2
from local_settings import DB

def get_conn():
    conn = psycopg2.connect(host=DB['HOST'], port=DB['PORT'], user=DB['USER'], password=DB['PASSWORD'],
        database=DB['NAME'])
    return conn


def execute_sql(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)


