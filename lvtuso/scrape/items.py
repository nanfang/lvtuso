# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class MafengwoPlace(Item):
    name = Field()
    hot = Field()
    lat = Field()
    lng = Field()
    p_id = Field()
    level = Field()
