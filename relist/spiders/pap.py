from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from relist.items import Property
import re


URL_TEMPLATE = "http://www.pap.fr/annonce/vente-appartements-paris-12e-g%s-jusqu-a-400000-euros-a-partir-de-40-m2"


class PAPSpider(CrawlSpider):

    name = 'pap'
    allowed_domains = ['pap.fr']
    start_urls = [URL_TEMPLATE % (37767 + int(postcode)) for postcode in "10 11 12 18 19 20".split(' ')]
    regex = r'http://www.pap.fr/annonce/vente-appartements-paris-.*-r\d{9}'
    rules = [Rule(LinkExtractor(allow=regex), 'parse_ad'),
        Rule(LxmlLinkExtractor(allow='.*', restrict_xpaths="//ul[contains(@class,'pagination')]/li[contains(@class,'next')]/a[contains(text(), 'Suivante')]"))]

    def parse_ad(self, response):
        pty = Property()
        pty['url'] = response.url
        pty['listed_on'] = 'pap'
        # Price
        prices = response.css('h1 span.prix').xpath('text()').extract()
        assert len(prices) == 1
        pty['price'] = int(prices[0].rstrip(u' $\u20ac').replace('.', ''))

        # Surface
        li = response.css('.footer-descriptif ul').xpath("//li[contains(span//text(), 'Surface')]").xpath("text()")
        # >>> li.xpath("text()").extract()
        # [u'\n\t\t\t\t\t\t\t\t', u'\n\t\t\t\t\t\t\t\t40\xa0', u'\t\t\t\t\t\t\t']
        assert len(li) == 3
        pty['size'] = float(li[1].extract().strip())

        # Post code
        titles = response.css('.text-annonce h2').xpath("text()").extract()
        assert len(titles) == 1
        match = re.search(r'\d{5}', titles[0])
        assert match is not None
        pty['postcode'] = int(match.group())
    
        # Content
        pty['title'] = response.css('h1 span.title').xpath('text()').extract()[0] + ' - ' + titles[0]
        pty['description'] = ' '.join(response.css('div.text-annonce p').xpath('text()').extract())

        # Price per square meter
        pty['ppsqm'] = float(pty['price']) / pty['size']

        return pty
    