from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor


class MaccosmeticsSpider(CrawlSpider):
    name = "maccosmetics"
    allowed_domains = ["maccosmetics.com"]
    start_urls = [
        "http://www.maccosmetics.com/bestsellers"
    ]

    rules = (
        Rule(LinkExtractor(
            # restrict_xpaths='//ul/li/a[contains(@href, "page")])'),
            allow=(r'.*Npp.*', )),
            callback='parse_items',
            follow=True
        ),
    )

    def parse_items(self, response):
        pass
