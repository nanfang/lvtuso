# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals, print_function
import simplejson as json
from scrapy.contrib.spiders.crawl import CrawlSpider
from lvtuso.scrape.items import MafengwoPlace

MUNICIPALITIES ={
    '10848': "北京市",
    '10849': "上海市",
    '10847': "天津市",
    '10846': "重庆市",
    '10845': "香港特别行政区",
    '10844': "澳门特别行政区",
}

PROVINCES = {
    '10025': "西藏",
    '10028': "云南",
    '10066': "内蒙古",
    '10081': "新疆",
    '10098': "山东",
    '10100': "江苏",
    '10104': "贵州",
    '10107': "四川",
    '10109': "山西",
    '10110': "青海",
    '10111': "浙江",
    '10112': "广西",
    '10114': "河南",
    '10115': "安徽",
    '10123': "湖南",
    '10153': "福建",
    '10224': "湖北",
    '10225': "河北",
    '10226': "辽宁",
    '10227': "甘肃",
    '10262': "黑龙江",
    '10263': "江西",
    '10324': "吉林",
    '10325': "海南",
    '10383': "广东",
    '10384': "陕西",
    '10441': "宁夏",
    '10074': "台湾",
}

LEVEL_CITY = 1
LEVEL_SPOT = 2

PLACE_BASE = 'http://www.mafengwo.cn/mdd/ajax_mdd.php?act=GetChildrenMdd&mddid=%s&page=%s'

class PlaceSpider(CrawlSpider):
    name = 'mafengwo-places'
    start_urls =  [PLACE_BASE % (id, 1) for id in PROVINCES.keys() + MUNICIPALITIES.keys()]

    def start_requests(self):
        for p_id in PROVINCES:
            yield self._request(LEVEL_CITY, p_id, 1)

        for p_id in MUNICIPALITIES:
            yield self._request(LEVEL_SPOT, p_id, 1)


    def parse(self, response):
        l = json.loads(response.body)['msg']['list']
        r = response.request
        if l:
            yield self._request(r.meta['level'], r.meta['p_id'], r.meta['page']+1)

        for p in l:
            place = MafengwoPlace()
            place['name'] = p['name']
            place['lat'] = p['lat']
            place['lng'] = p['lng']
            place['hot'] = p['hot']
            place['p_id'] = r.meta['p_id']
            place['level'] = r.meta['level']
            yield place

    def _request(self, level, p_id,  page):
        r = self.make_requests_from_url(PLACE_BASE % (p_id, page))
        r.meta['level'] = level
        r.meta['p_id'] = p_id
        r.meta['page'] = page
        return r


