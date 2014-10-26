from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from relist.items import Property


URL_TEMPLATE = "http://www.leboncoin.fr/ventes_immobilieres/offres/ile_de_france/?f=a&th=1&pe=15&sqs=5&ret=2&location=Paris%%20%s"


class LBCSpider(CrawlSpider):

    name = 'leboncoin'
    allowed_domains = ['leboncoin.fr']
    start_urls = [URL_TEMPLATE % postcode for postcode in "75010 75011 75012 75018 75019 75020".split(' ')]
    regex = r'http://www\.leboncoin\.fr/ventes_immobilieres/\d+.htm\?ca=12_s'
    rules = [Rule(LinkExtractor(allow=regex), 'parse_ad'),
        Rule(LxmlLinkExtractor(allow='.*', restrict_xpaths="//nav/ul/li/a[contains(text(), 'Page suivante')]"))]

    def parse_ad(self, response):
        pty = Property()
        pty['url'] = response.url

        # Price
        prices = response.css('span.price').xpath('text()').extract()
        assert len(prices) == 1
        pty['cost'] = int(prices[0].rstrip(u' $\u20ac').replace(' ', ''))

        # Surface
        row = response.css('.lbcParams.criterias').xpath("//tr[contains(th//text(), 'Surface')]")
        surfaces = row.xpath('td/text()').extract()
        assert len(surfaces) == 1
        pty['size'] = float(surfaces[0].rstrip(' mM'))

        # Post code
        row = response.css('.lbcParams.criterias').xpath("//tr[contains(th//text(), 'Code postal')]")
        postcodes = row.xpath('td/text()').extract()
        assert len(postcodes) == 1
        pty['postcode'] = int(postcodes[0])
    
        # Content
        pty['title'] = response.css('#ad_subject').xpath('text()').extract()[0]
        pty['description'] = ' '.join(response.css('div.AdviewContent div.content').xpath('text()').extract())

        # Price per square meter
        pty['ppsqm'] = float(pty['cost']) / pty['size']

        return pty
    