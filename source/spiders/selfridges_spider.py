import scrapy
from scrapy.spiders import CrawlSpider
# from scrapy.utils.response import get_base_url

from source.items import ProductItem
import urlparse


class SelfridgesSpider(CrawlSpider):
    name = "selfridges"
    allowed_domains = ["selfridges.com"]
    start_urls = [
        'http://www.selfridges.com/GB/en/cat/beauty/make-up/eyes/?llc=sn',
        'http://www.selfridges.com/GB/en/cat/beauty/make-up/face/?llc=sn',
        'http://www.selfridges.com/GB/en/cat/beauty/make-up/make-up-brushes-tools/?llc=sn',
        'http://www.selfridges.com/GB/en/cat/beauty/make-up/lips/?llc=sn',
        'http://www.selfridges.com/GB/en/cat/beauty/make-up/nails/?llc=sn',
        'http://www.selfridges.com/GB/en/cat/beauty/fragrance/?llc=sn',
        'http://www.selfridges.com/GB/en/cat/beauty/skincare/?llc=sn',
        'http://www.selfridges.com/GB/en/cat/beauty/bath-bodycare/?llc=sn',
        'http://www.selfridges.com/GB/en/cat/beauty/mens-grooming/?llc=sn',
        'http://www.selfridges.com/GB/en/cat/beauty/mens-grooming/?llc=sn',
    ]

    # rules = (
    #     Rule(LinkExtractor(
    #         # restrict_xpaths='//ul/li/a[contains(@href, "page")])'),
    #         allow=(r'.*pn=.*', )),
    #         callback='parse_items',
    #         follow=True
    #     ),
    #     # Rule(LinkExtractor(
    #     #     restrict_xpaths='//ul[@class="refineItemOptions"][0]/li/a'),
    #     #     # allow=(),
    #     #     callback='parse_category',
    #     #     follow=True
    #     # ),
    # )

    def parse_start_url(self, response):
        print("entered")
        categories = response.xpath(
            '//div[contains(@class, "sectionCategory")]//li//a')
        all_links = []
        for each_category in categories:
            full_url = urlparse.urljoin(
                response.url, each_category.xpath("./@href").extract_first().strip())
            my_request = scrapy.Request(
                full_url,
                self.parse_items)
            my_request.meta['category'] = {
                "sub_category": each_category.xpath(
                    './span[@class="label"]/text()'
                ).extract_first().strip(),
                "category": response.xpath(
                    '//h3[@class="categoryTitle"]/a/text()'
                ).extract_first().strip()
            }
            print ("meta", my_request.meta)
            all_links.append(my_request)
        print(all_links)
        return all_links

    def parse_items(self, response):
        print "------------"
        print(response.url)
        print("----------")
        all_items = response.xpath('//div[@class="productContainer"]')
        category = response.meta['category']['category']
        sub_category = response.meta['category']['sub_category']
        for each_item in all_items:
            brand = each_item.xpath('//a[@class="title"]/text()').extract_first().strip()
            name = each_item.xpath('//a[@class="description"]/text()').extract_first().strip()
            price = each_item.xpath('//p[@class="price"]/text()').extract_first().strip()
            affiliate_link = each_item.xpath('./a/@href').extract_first().split()
            website = "selfridges.com"
            image_urls = [
                each_item.xpath(
                    '//div[@class="productContainer"]//img/@data-mainsrc'
                ).extract_first().strip()
            ]
            # price not found on hold
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
        next_link = response.xpath('//div[@class="pageNumberInner"]//a/@href').extract_first()
        my_request = scrapy.Request(
            next_link,
            self.parse_items)
        my_request.meta['category'] = {
            "sub_category": sub_category,
            "category": category,
        }
        yield my_request
