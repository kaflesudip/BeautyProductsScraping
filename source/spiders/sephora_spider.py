from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from source.items import ProductItem


class CultbeautySpider(CrawlSpider):
    name = "sephora"
    allowed_domains = ["sephora.com"]
    start_urls = [
        'http://www.sephora.com/skincare'
    ]

    rules = (
        Rule(LinkExtractor(
            # restrict_xpaths='//ul/li/a[contains(@href, "page")])'),
            allow=(r'.*Npp.*', )),
            callback='parse_items',
            follow=True
        ),
    )

    def parse_start_url(self, response):
        return self.parse_items(response)

    def parse_items(self, response):
       pass