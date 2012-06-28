# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals, print_function
from redis import Redis

if __name__ == '__main__':
    r = Redis()
    r.zadd(u'北京', 104324, 100)


    print(r.zrevrange(u'北京', 0, 50, True))