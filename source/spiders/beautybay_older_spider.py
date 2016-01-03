from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
import scrapy


class BeautybaySpider(CrawlSpider):
    name = "beautybay"
    allowed_domains = ["beautybay.com"]
    start_urls = [
        "http://www.beautybay.com/cosmetics/_/N-23Z1xZ1wZ1vZ1uZ1tZo/",
        "http://www.beautybay.com/skincare/_/N-23Z1xZ1wZ1vZ1uZ1tZo/",
        "http://www.beautybay.com/bathandbody/_/N-23Z1xZ1wZ1vZ1uZ1tZo/",
        "http://www.beautybay.com/haircare/_/N-23Z1xZ1wZ1vZ1uZ1tZo/",
        "http://www.beautybay.com/nailcare/_/N-23Z1xZ1wZ1vZ1uZ1tZo/",
        "http://www.beautybay.com/electrical/_/N-23Z1xZ1wZ1vZ1uZ1tZo/",
        "http://www.beautybay.com/accessories/_/N-23Z1xZ1wZ1vZ1uZ1tZo/",

    ]

    rules = (
        Rule(LinkExtractor(
            # restrict_xpaths='//ul/li/a[contains(@href, "page")])'),
            allow=(r'.*Npp.*', )),
            callback='parse_items',
            follow=True
        ),
    )

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse, meta={
                'splash': {
                    'endpoint': 'render.html',
                    'args': {'wait': 10}
                }
            })

    def parse_start_url(self, response):
        return self.parse_items(response)

    def parse_items(self, response):
        print("done")
        print(response.body)
