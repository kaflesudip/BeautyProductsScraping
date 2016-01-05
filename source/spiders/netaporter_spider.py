import urlparse
import scrapy
from scrapy.spiders import CrawlSpider
# from scrapy.utils.response import get_base_url

from source.items import ProductItem


# http://www.net-a-porter.com/np/en/d/shop/Beauty/Bath_and_Body?image_view=product&pn=1&npp=60&navlevel3=Body_Cleanser_and_Soap&dScroll=0


makeup_categories = {
    "Face": [
        "BB Cream",
        "Blush",
        "Bronzer",
        "Concealer",
        "Contour",
        "Foundation",
        "Illuminator",
        "Powder",
        "Primer",
        "Tinted Moisturizer",
    ],

    "Eye": [
        "Brows",
        "Eyeliner",
        "Eyeshadow",
        "Mascara",
    ],
    "Lip": [
        "Lipcare",
        "Lipgloss",
        "Lipliner",
        "Lipstick",
    ],
    "Multi-Purpose": [
        "SPF",
        "Palettes",
    ],
    "Brushes and Tools": [
        "Removers",
        "Sets",
    ]
}


class NetaporterSpider(CrawlSpider):
    name = "netaporter"
    allowed_domains = ["net-a-porter.com"]
    custom_settings = {"IMAGES_STORE": '../images/netaporter'}

    start_urls = [
        'http://www.net-a-porter.com/np/en/d/shop/Beauty/Bath_and_Body',
        'http://www.net-a-porter.com/np/en/d/shop/Beauty/Beauty_Sets?',
        'http://www.net-a-porter.com/np/en/d/shop/Beauty/Candles?',
        'http://www.net-a-porter.com/np/en/d/shop/Beauty/Cosmetics_Cases?',
        'http://www.net-a-porter.com/np/en/d/shop/Beauty/Fragrance?',
        'http://www.net-a-porter.com/np/en/d/shop/Beauty/Haircare?',
        'http://www.net-a-porter.com/np/en/d/shop/Beauty/Makeup?',
        'http://www.net-a-porter.com/np/en/d/shop/Beauty/Nails?',
        'http://www.net-a-porter.com/np/en/d/shop/Beauty/Skincare?',
        'http://www.net-a-porter.com/np/en/d/shop/Beauty/Tools_and_Devices?',
    ]

    def parse_start_url(self, response):
        category = response.xpath(
            '//li[contains(@class, " selected")]/a/span/text()').extract_first()
        all_categories = response.xpath('//ul[@id="navLevel3-filter"]//a[@class="filter-item"]')
        all_links = []
        for each_link in all_categories:
            print("each_link", each_link)
            new_url = each_link.xpath("./@href").extract_first()
            full_url = urlparse.urljoin(response.url, new_url)
            sub_category = each_link.xpath('./span[@class="filter-name"]/text()').extract_first()
            if sub_category.strip() in makeup_categories.keys():
                continue
            for cat, sub_categories in makeup_categories.iteritems():
                if sub_category in sub_categories:
                    category = cat
                    break
            my_request = scrapy.Request(
                full_url,
                self.parse_items)
            my_request.meta['category'] = {
                "sub_category": sub_category,
                "category": category
            }
            print ("meta", my_request.meta)
            print(full_url, "link")
            all_links.append(my_request)
        print(all_links)
        return all_links

    def parse_items(self, response):
        print "------------"
        print(response.url)
        print("----------")
        category = response.meta['category']['category']
        sub_category = response.meta['category']['sub_category']
        all_items = response.xpath('//ul[@class="products"]/li')
        print(all_items, len(all_items))
        for each_item in all_items:
            name = ''.join(each_item.xpath(
                './/div[@class="description"]/text()').extract()).strip()
            brand = each_item.xpath('.//span[@class="designer"]/text()').extract_first().strip()
            price = each_item.xpath('.//span[@class="price "]/text()').extract_first().strip()
            image_urls = ["http:" + each_item.xpath(".//img/@data-src").extract_first()]
            print(image_urls)
            affiliate_link = urlparse.urljoin(
                response.url, each_item.xpath(".//a/@href").extract_first())
            website = "net-a-porter.com"
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
        next_link = response.xpath('//a[@class="next-page"]/@href').extract_first()
        if next_link:
            full_url = urlparse.urljoin(response.url, next_link)
            my_request = scrapy.Request(
                full_url,
                self.parse_items)
            my_request.meta['category'] = {
                "sub_category": sub_category,
                "category": category,
            }
            yield my_request
