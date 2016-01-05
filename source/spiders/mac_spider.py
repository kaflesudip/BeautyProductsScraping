import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
# from urllib.parse import urlparse
# from scrapy.utils.response import get_base_url

from source.items import ProductItem


class MacSpider(CrawlSpider):
    name = "Macspider"
    custom_settings = {"IMAGES_STORE": '../images/mac'}

    allowed_domains = ["www.maccosmetics.com"]
    start_urls = [
        'http://www.maccosmetics.com',
        # 'https://www.beautylish.co.uk/make-up.html?ref=mm',
        # 'https://www.beautylish.co.uk/fragrance.html?ref=mm',
        # 'https://www.beautylish.co.uk/hair-care.html?ref=mm',
        # 'https://www.beautylish.co.uk/bath-body.html?ref=mm',
        # 'https://www.beautylish.co.uk/wellbeing.html?ref=mm',
    ]

    rules = [
        Rule(
            LxmlLinkExtractor(
                allow=(),
                deny=(),
                restrict_xpaths=(
                    '//li[contains(@class,"mm-subnav-item-v1")][position()<5]//div[@class="site-navigation__submenu-col"]//a'
                )
            ),
            callback="parse_category",
            follow=True,
        )
    ]

   

    def parse_category(self, response):
        # print "response", response.url, 'endresponse'
        # http://www.maccosmetics.com/products/13840/Products/Makeup/Eyes/Shadow
        # http://www.maccosmetics.com/products/13825/Products/Primer-Skincare/Primers
        # if response.url in [
        #     'http://www.maccosmetics.com/products/13840/Products/Makeup/Eyes/Shadow',
        #     'http://www.maccosmetics.com/products/13825/Products/Primer-Skincare/Primers']:
        my_url = response.url
        test1 = my_url.split('/')
        test1 = [each for each in test1 if len(each) != 0]
        category = test1[len(test1) - 2]
        sub_category = test1[len(test1) - 1]
        sel = Selector(response)
        extract_product = sel.xpath('//div[@class="product__detail"]')
        website = "http://www.maccosmetics.com"
        brand = "MAC"
        for each_product in extract_product:
            name = each_product.xpath(".//header//h3[@class='product__name']/text()").extract_first()
            affiliate_link = website + "/" + each_product.xpath('.//header[@class="product__header"]//a[@class="product__name-link"]/@href').extract_first()
            try:
                image_urls = "http://www.maccosmetics.com/" + each_product.xpath('.//img[contains(@class,"product__sku")]/@src').extract_first()
            except:
                pass
            image_urls = [str(image_urls)]
            price = each_product.xpath(".//header[@class='product__header']//div[@class='product__price']/text()").extract_first()

            item = ProductItem(
                name=name.strip(),
                price=price.strip(),
                image_urls=image_urls,
                brand=brand,
                affiliate_link=affiliate_link,
                category=category,
                sub_category=sub_category,
                website=website
            )

            yield item
