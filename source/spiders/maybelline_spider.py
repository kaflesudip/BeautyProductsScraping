import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
# from scrapy.utils.response import get_base_url

from source.items import ProductItem
import urlparse


class MaybellineSpider(CrawlSpider):
    name = "maybelline"
    allowed_domains = ["maybelline.co.uk"]
    start_urls = [
        'http://www.maybelline.co.uk/makeup/eye.aspx?origin=Footer-CategoryLink',
        'http://www.maybelline.co.uk/makeup/face.aspx?origin=Footer-CategoryLink',
        'http://www.maybelline.co.uk/makeup/lip.aspx?origin=Footer-CategoryLink',
        'http://www.maybelline.co.uk/makeup/nail.aspx?origin=Footer-CategoryLink',
        'http://www.maybelline.co.uk/makeup/accessories.aspx?origin=Footer-CategoryLink',
    ]

    rules = (
        Rule(LinkExtractor(
            # restrict_xpaths='//ul/li/a[contains(@href, "page")])'),
            allow=(r'.*Npp.*', )),
            callback='parse_items',
            follow=True
        ),
        # Rule(LinkExtractor(
        #     restrict_xpaths='//ul[@class="refineItemOptions"][0]/li/a'),
        #     # allow=(),
        #     callback='parse_category',
        #     follow=True
        # ),
    )

    def parse_start_url(self, response):
        print("entered")
        categories = response.xpath(
            '//ul[@class="category-subnav-links filters"]//li//a')
        all_links = []
        category = response.xpath(
            '//h1[@class="title"]/text()'
        ).extract_first().replace("Makeup", "").strip()
        for each_category in categories:
            full_url = urlparse.urljoin(response.url, each_category.xpath("./@href").extract_first())
            my_request = scrapy.Request(
                full_url,
                self.parse_items)
            my_request.meta['category'] = {
                "sub_category": each_category.xpath("./text()").extract_first(),
                "category": category
            }
            print ("meta", my_request.meta)
            all_links.append(my_request)
        print(all_links)
        return all_links

    def parse_items(self, response):
        print("---------------------------------------------")
        category = response.meta['category']['category']
        sub_category = response.meta['category']['sub_category']
        print(category, sub_category)
        print("--------------------------------")
        products = response.xpath('//li[@class="product"]')
        for each_item in products:
            name = each_item.xpath(".//h3/a/text()").extract_first()
            price = ""
            brand = "maybelline"
            affiliate_link = each_item.xpath(".//h3/a/@href").extract_first()
            sub_category = sub_category
            category = category
            website = "maybelline.com"
            image_urls = [
                urlparse.urljoin(response.url, response.xpath(".//img/@src").extract_first())]
            item = ProductItem(
                name=name.strip(),
                price=price.strip(),
                image_urls=image_urls,
                brand=brand.strip(),
                affiliate_link=affiliate_link,
                category=category,
                sub_category=sub_category,
                website=website
            )
            yield item
