from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import signals
from scrapy.utils.project import get_project_settings


class Scraper(object):

    def __init__(self, sites=None):
        settings = get_project_settings()
        base_crawler = Crawler(settings)
        spider_names = base_crawler.spiders.list()
        if sites is not None:
            spider_names = [s for s in sites if s in spider_names]

        self.running = len(spider_names)

        for spider_name in spider_names:
            crawler = Crawler(settings)
            crawler.configure()
            spider = crawler.spiders.create(spider_name)
            crawler.crawl(spider)
            crawler.signals.connect(self.unlock, signal=signals.spider_closed)
            crawler.start()

        reactor.run() # this will block until all spider_closed signal are sent

    def unlock(self):
        self.running -= 1
        if self.running <= 0:
            reactor.stop()
