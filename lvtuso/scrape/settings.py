# Scrapy settings for scrape project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'Lvtuso Search Engine (http://lvtuso.com)'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['lvtuso.scrape.spiders']
NEWSPIDER_MODULE = 'lvtuso.scrape.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

ITEM_PIPELINES = [
    'lvtuso.scrape.pipelines.MFWPipeline',
]