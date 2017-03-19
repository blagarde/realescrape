from twisted.internet import reactor
from scrapy.crawler import Crawler, CrawlerProcess
from scrapy import signals
from scrapy.utils.project import get_project_settings
from relist.spiders import lbc, pap, seloger


SPIDERS = {
    "lbc": lbc.LBCSpider,
    "pap": pap.PAPSpider,
    "seloger": seloger.SeLogerSpider,
}


class Scraper(object):

    def __init__(self, sites=SPIDERS.keys()):
        spiders = {k:v for k, v in SPIDERS.items() if k in sites}
        process = CrawlerProcess()
        for s in spiders.values():
            process.crawl(s)
        process.start()
