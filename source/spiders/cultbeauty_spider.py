from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from source.items import ProductItem


class CultbeautySpider(CrawlSpider):
    name = "cultbeauty"
    allowed_domains = ["cultbeauty.com"]
    start_urls = [
        'https://www.cultbeauty.co.uk/skin-care.html?ref=mm'
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
        category = response.xpath('//title/text()').extract_first()
        mobile_items = response.xpath('//div[@class="productGridItem"]')
        # file_ = open('Failed.html', 'w')
        # file_.write(response.body)
        # file_.close()
        for mobile_item in mobile_items:
            image_url = "http:" + mobile_item.xpath('.//img/@src').extract_first()
            name = mobile_item.xpath('.//h3/text()').extract_first()
            brand = mobile_item.xpath(
                './/div[contains(@class, "productGridBrandTitle")]/span/text()').extract_first()
            price = mobile_item.xpath(
                './/div[@class="priceBox"]/span/text()').extract_first().encode('utf-8')
            website = 'http://www.cultbeauty.co.uk'
            # affiliate_link = website +\
            #     "/" + str(mobile_item.xpath('.//a').extract_first())
            affiliate_link = website + "/" + mobile_item.xpath('.//a/@href').extract_first()
            item = ProductItem(
                name=name.strip(),
                price=price.strip(),
                image_url=image_url,
                brand=brand.strip(),
                affiliate_link=affiliate_link,
                category=category,
                website=website
            )
            yield item
