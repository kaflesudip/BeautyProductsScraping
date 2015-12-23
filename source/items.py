# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    # name, brand name, image, price and category
    name = scrapy.Field()
    price = scrapy.Field()
    category = scrapy.Field()
    sub_category = scrapy.Field()
    affiliate_link = scrapy.Field()
    website = scrapy.Field()
    brand = scrapy.Field()
    images = scrapy.Field()
    image_urls = scrapy.Field()
