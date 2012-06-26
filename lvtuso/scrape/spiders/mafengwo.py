# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals, print_function
import re
from scrapy.selector.lxmlsel import HtmlXPathSelector
import simplejson as json
from scrapy.contrib.spiders.crawl import CrawlSpider
from lvtuso.scrape.items import MafengwoPlace
from lvtuso.constants import PLACE_LEVEL

MUNICIPALITIES ={
    '10848': "北京",
    '10849': "上海",
    '10847': "天津",
    '10846': "重庆",
    '10845': "香港",
    '10844': "澳门",
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


BASE_URL = 'http://www.mafengwo.cn'
BASE_MDD = BASE_URL + '/mdd/ajax_mdd.php?act=GetChildrenMdd&mddid=%s&page=%s'
BASE_JD = BASE_URL + '/jd/%s/'

class PlaceSpider(CrawlSpider):
    name = 'mafengwo-places'

    def __init__(self, *a, **kw):
        super(PlaceSpider, self).__init__(*a, **kw)
        self.errors=[]

    def add_error(self, item, error):
        self.errors.append((item, error))

    def start_requests(self):
        for mddid in PROVINCES:
            yield self._mdd_request(PLACE_LEVEL.PROVINCE, mddid, 1)

        for mddid in MUNICIPALITIES:
            yield self._mdd_request(PLACE_LEVEL.CITY, mddid, 1)


    def _parse_mdds(self, response):
        r = response.request
        l = json.loads(response.body)['msg']['list']
        if l:
            yield (self._mdd_request(r.meta['level'], r.meta['mddid'], r.meta['page'] + 1))
            for p in l:
                if r.meta['level'] == PLACE_LEVEL.CITY:
                    if p['name'] != r.meta['name']:
                        # for city, we don't scrape its spot in mdd but in jd
                        continue

                place = MafengwoPlace()
                place['name'] = p['name']
                place['lat'] = p['lat']
                place['lng'] = p['lng']
                place['hot'] = p['hot']
                place['id'] = p['mddid']
                place['p_id'] = r.meta['mddid']
                place['p_level'] = r.meta['level']
                place['level'] = r.meta['level'] if place['name'] == r.meta['name'] else self._sub_level(r.meta['level'])
                yield place
                yield self._jd_request(place['level'], place['id'], place['name'])

    def _parse_jd(self, response):
        r = response.request
        hxs = HtmlXPathSelector(response)
        items = hxs.select("//li[@class='item']/div[@class='store']")
        if items:
            yield self._jd_request(r.meta['level'], r.meta['id'], r.meta['name'], r.meta['page']+1)
        for item in items:
            name = item.select('.//h3/a/text()').extract()[0]
            rating = item.select(".//div[@class='rank']/span/@class").extract()[0]
            tags = item.select(".//div[@class='tag']/a/text()").extract()
            path = item.select('.//h3/a/@href').extract()[0]
            place = MafengwoPlace()
            place['name'] = name
            if rating:
                place['rating'] = int(rating[4:])

            place['tags'] = tags
            place['id'] = self._extract_id(path)
            place['p_id'] = r.meta['id']
            place['level'] = self._sub_level(r.meta['level'])

            yield self._jd_detail_request(place, path)

    def _extract_coordinate(self, response):
        m = re.match(r'^[\s\S]*lat:"(.+)",\s*lng:"(.+)",[\s\S]*$', response.body)
        return m.group(1), m.group(2)

    def _parse_jd_detail(self, response):
        r = response.request
        place = r.meta['place']
        lat, lng = self._extract_coordinate(response)
        place['lng'] = lng
        place['lat'] = lat
        yield place


    def _jd_detail_request(self, place, path):
        r = self.make_requests_from_url(BASE_URL + path)
        r.meta['place'] = place
        r.callback = self._parse_jd_detail
        return r


    def _extract_id(self, path):
        return int(re.match(r'.*/(\d+)\.html$', path).group(1))

    def _sub_level(self, level):
        return level << 1

    def _mdd_request(self, level, mddid,  page):
        r = self.make_requests_from_url(BASE_MDD % (mddid, page))
        r.callback = self._parse_mdds
        r.meta['level'] = level
        r.meta['mddid'] = mddid
        r.meta['name'] = MUNICIPALITIES.get(mddid) or PROVINCES.get(mddid)
        r.meta['page'] = page
        r.meta['type'] = 'mdd'

        return r

    def _jd_request(self, level, id, name,  page=1):
        url = BASE_JD % id
        if page > 1:
            url += '%s.html' % page
        r = self.make_requests_from_url(url)
        r.callback = self._parse_jd

        r.meta['level'] = level
        r.meta['id'] = id
        r.meta['name'] = name
        r.meta['page'] = page
        r.meta['type'] = 'jd'

        return r
