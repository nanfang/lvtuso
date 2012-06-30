# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals, print_function
import re
import os
import django.utils.simplejson as json
from django.core.management.base import BaseCommand

from lvtuso import storage
from lvtuso import settings
from lvtuso.common.pinyin import Pinyin
from lvtuso.constants import STORE_KEYS

py = Pinyin(data_path=os.path.join(settings.PROJECT_ROOT, "data/Mandarin.dat" ))
p = re.compile(ur'(.*)（(.*)）')

class Command(BaseCommand):
    help = 'build index of typeahead'

    def handle(self, *args, **options):
        conn = storage.get_conn()
        redis = storage.get_redis()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, hot, rating FROM place_mfw')
        for id, name, hot, rating in cursor:
            info = [name, hot, rating]
            redis.hset(STORE_KEYS.PLACE_INFO, str(id), json.dumps(info))

            prefixes = _extract_prefixes(name)
            score = _score(hot, rating)
            for prefix in prefixes:
                redis.zadd(STORE_KEYS.PLACE_TYPE_AHEAD % prefix, score, id)
                print('%s %s %s' % (prefix, score, id))

def _str_prefix(name):
    prefixes = set()
    for i in range(len(name)):
        prefix = name[:i + 1]
        prefixes.add(prefix)
        prefixes.add(py.pinyin_first(prefix))
    name_py = py.pinyin(name)
    for i in range(len(name_py)):
        prefix = name_py[:i + 1]
        prefixes.add(prefix)
    return prefixes

def _extract_prefixes(name):
    prefixes = set()
    m = p.match(name)
    name, alias = (m.group(1), m.group(2)) if m else (name, None)
    prefixes.update(_str_prefix(name))
    if alias:
        prefixes.update(_str_prefix(alias))
    return prefixes

def _score(hot, rating):
    hot = hot or 0
    rating = (rating / float(10)) if rating else 0
    return hot + rating
