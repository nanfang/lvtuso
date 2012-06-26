# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class MafengwoPlace(Item):
    id = Field()
    name = Field()
    hot = Field()
    lat = Field()
    lng = Field()
    level = Field()
    rating = Field()
    tags = Field()

    p_id = Field()
    p_level = Field()
