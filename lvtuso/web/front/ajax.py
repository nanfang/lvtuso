# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals, print_function
from django.http import HttpResponse
import django.utils.simplejson as json
from lvtuso import storage
from lvtuso.constants import STORE_KEYS
from lvtuso.web.decorators import ajax_call

@ajax_call
def typeahead(request):
    return HttpResponse(json.dumps(_prefix_search_places(request.GET.get('q'))),'application/javascript')

def _find_places_by_ids(ids):
    redis = storage.get_redis()
    places = redis.hmget(STORE_KEYS.PLACE_INFO, [int(id) for id in ids])
    places = [json.loads(p) for p in places]
    for idx, p in enumerate(places):
        p.insert(1, ids[idx])
    return places


def _prefix_search_places(prefix):
    prefix = prefix.strip() if prefix else None
    if not prefix:
        return []
    redis = storage.get_redis()
    return _find_places_by_ids(redis.zrevrange(STORE_KEYS.PLACE_TYPE_AHEAD % prefix, 0, 20))

if __name__ == '__main__':
    print('北京'.lower())

