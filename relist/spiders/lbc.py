from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from relist.items import Property



url = "http://www.leboncoin.fr/ventes_immobilieres/offres/ile_de_france/?f=a&th=1&pe=15&sqs=5&ret=2&location=Paris%2075010%2CParis%2075011%2CParis%2075012"


class LBCSpider(CrawlSpider):

    name = 'leboncoin'
    allowed_domains = ['leboncoin.fr']
    start_urls = [url]
    regex = r'http://www\.leboncoin\.fr/ventes_immobilieres/\d+.htm\?ca=12_s'
    rules = [Rule(LinkExtractor(allow=regex), 'parse_ad')]

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
        pty['description'] = response.css('div.AdviewContent div.content').xpath('text()').extract()

        return pty
    