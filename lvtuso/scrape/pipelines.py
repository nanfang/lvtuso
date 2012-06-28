from __future__ import division, unicode_literals, print_function
from lvtuso.scrape.items import MafengwoPlace
from lvtuso import storage
from lvtuso.common import dbutils
from lvtuso.scrape.spiders import mafengwo

class MFWPipeline(object):
    def __init__(self):
        super(MFWPipeline, self).__init__()
        self.conn = storage.get_conn()

    def process_item(self, item, spider):
        try:
            if isinstance(item, MafengwoPlace):
                self._save_space(item)
        except Exception:
            self.conn.rollback()
            item['id'] = -item['id']
            try:
                self._save_space(item)
            except Exception as ex:
                print(ex)
                spider.add_error(item, ex)
        return item

    def close_spider(self, spider):
        if isinstance(spider, mafengwo.PlaceSpider) and spider.errors:
            for item, error in spider.errors:
                print('--------------------------------')
                print('error to save %s' % item['name'])
                print(item)
                print(error)


    def _save_space(self, item):
        dbutils.execute(self.conn,
            """
            INSERT INTO place_mfw(id, p_id, name, hot, rating, level, tags, location)
            values ( %%s, %%s, %%s, %%s, %%s, %%s, %%s, ST_GeomFromText('POINT(%s %s)', 4326))
            """ % (item.get('lng'), item.get('lat')),
            (item.get('id'), item.get('p_id'), item.get('name'), item.get('hot'), item.get('rating'), item.get('level'),
             item.get('tags') ))
        self.conn.commit()
        print('%s saved' % item.get('name'))
