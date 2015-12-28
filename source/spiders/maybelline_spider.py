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
            '//ul[@class="category-subnav-links filters"]/li/h2/a/')
        all_links = []
        for each_category in categories:
            full_url = urlparse.urljoin(response.url, each_category.xpath("./@href").extract())
            my_request = scrapy.Request(
                full_url,
                self.parse_items)
            my_request.meta['category'] = {
                "sub_category": each_category.xpath("./text()").extract(),
                "category": response.xpath('//h1[@class="title"]').extract()
            }
            print ("meta", my_request.meta)
            all_links.append(my_request)
        print(all_links)
        return all_links

    def parse_items(self, response):
        # price not found on hold
        # item = ProductItem(
        #     name=name.strip(),
        #     price=price.strip(),
        #     image_urls=image_urls,
        #     brand=brand.strip(),
        #     affiliate_link=affiliate_link,
        #     category=category,
        #     sub_category=sub_category,
        #     website=website
        # )
        # yield item

        to_replace = response.meta['to_replace']
        next_number = int(to_replace.replace("currentPage=", "")) + 1
        next_link = response.url.replace(
            to_replace, "currentPage=" + str(next_number))
        my_request = scrapy.Request(
            next_link,
            self.parse_items)
        my_request.meta['category'] = {
            "sub_category": sub_category,
            "category": category,
            "to_replace": "currentPage=" + str(next_number)
        }
        yield my_request
