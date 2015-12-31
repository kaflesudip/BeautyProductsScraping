import urllib
import scrapy
from scrapy.spiders import CrawlSpider
# from scrapy.utils.response import get_base_url

from source.items import ProductItem

ALL_BRANDS = ["Anastasia Beverly hills", "Avon", "Bare Escentuals", "Benefit", "Bobbi Brown", "Chanel", "Clarins", "Clinique", "Christian Dior", "Estee Lauder", "KatVonD", "Lancome",
              "Laura Mercier", "LOREAL", "Mac", "Maybelline", "Nars", "Nivea", "Olay", "Revlon", "Rimmel", "Smashbox", "Tarte", "Tom Ford", "Too faced", "Urban decay", "Yves saint Laurent (YSL)"
            "NYX",
]

ALL_CATEGORIES = {
    "EYES": [
        "Eye Shadow",
        "Liner",
        "Mascara",
        "Brows",
        "Lashes",
        "Eye Primer",
    ],
    "FACE": [
        "Foundation",
        "Powder",
        "Blush",
        "Concealer",
        "Bronzer",
        "Contour",
        "Face Highlight",
        "Face Primer",
    ],
    "LIPS": [
        "Lipstick",
        "Lip Gloss",
        "Lip liner",
        "Lip Balm",
        "Lip Stain Lip Care",
        "Oil Sets",
    ],
    "TOOLS": [
        "Brushes",
        "Sponges",
        "Pouches",
    ],
    "SKINCARE": [
        "Moisturiser",
        "Wash",
        "Mask",
        "Toner",
    ],
    "NAILS": [
        "Nail Polish ",
        "Nail Care",
    ]
}

# url_to_use = 'http://www.polyvore.com/cgi/shop?.in=json&.out=jsonx&request=%7B%22page"%3A{0}%2C22query%22%3A%22{1}%22%2C%22.passback%22%3A%7B%22idx_search%22%3A120%2C%22grid_idx_1x1%22%3A120%7D%7D'
url_to_use = 'http://www.polyvore.com/cgi/shop?.in=json&.out=jsonx&request=%7B%22page%22%3A{0}%2C%22query%22%3A%22{1}%22%2C%22.passback%22%3A%7B%22idx_search%22%3A120%2C%22grid_idx_1x1%22%3A120%7D%7D'

class PolyvoreSpider(CrawlSpider):
    name = "polyvore"
    allowed_domains = ["polyvore.com"]
    start_urls = [
        'http://www.polyvore.com/'
    ]

    def parse_start_url(self, response):
        all_links = []
        for each_category, sub_categories in ALL_CATEGORIES.iteritems():
            for sub_category in sub_categories:
                full_url = url_to_use.format("1", urllib.quote(sub_category))
                my_request = scrapy.Request(
                    full_url,
                    self.parse_items)
                my_request.meta['category'] = {
                    "sub_category": sub_category,
                    "category": each_category
                }
                print ("meta", my_request.meta)
                all_links.append(my_request)
        print(all_links)
        return all_links

    def parse_items(self, response):
        print "------------"
        print(response.url)
        print("----------")
        from scrapy.selector import Selector
        import json
        category = response.meta['category']['category']
        sub_category = response.meta['category']['sub_category']

        response_json = json.loads(response.body)
        required_text = response_json["result"]["html"]
        response = Selector(text=required_text)
        all_items = response.xpath('//div[contains(@class, "grid_item")]')
        for each_item in all_items:
            name = each_item.xpath('.//div[@class="title"]/a/text()').extract_first()
            price = each_item.xpath('.//span[@class="price"]/text()').extract_first()
            image_urls = [each_item.xpath(".//img/@src").extract_first()]
            affiliate_link = each_item.xpath(".//a/@href").extract_first()
            website = "polyvore.com"
            brand = [i for i in ALL_BRANDS if i.lower() in name.lower()]
            if brand:
                brand = brand[0]
                print ("brand", brand)
            else:
                print (name, brand, "exited")
                continue
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
        if response_json["result"]["more_pages"] == "1":
            next_page = int(response_json["result"]["page"]) + 1
        else:
            return
        next_link = url_to_use.format(str(next_page), urllib.quote(sub_category))
        my_request = scrapy.Request(
            next_link,
            self.parse_items)
        my_request.meta['category'] = {
            "sub_category": sub_category,
            "category": category,
        }
        yield my_request
