# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals, print_function
import logging
import user
import psycopg2
from redis.client import StrictRedis
from lvtuso import settings

_logger = logging.getLogger(__name__)
_redis = StrictRedis()
_conn = None

def get_redis():
    return _redis

# only use this in backend, use django connection in front end
def get_conn():
    global _conn
    if _conn:
        try:
            cur = _conn.cursor()
            cur.execute('SELECT 1')
        except Exception:
            _logger.debug('Connection is invalid', exc_info=True)
            _init_conn()
        finally:
            pass
    else:
        _init_conn()
    return _conn


def _init_conn():
    global _conn
    db = settings.DATABASES['default']
    _conn = psycopg2.connect(
        host=db['HOST'],
        user=db['USER'],
        password=db['PASSWORD'],
        database=db['NAME'])

