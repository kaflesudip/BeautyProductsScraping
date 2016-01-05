import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
# from scrapy.utils.response import get_base_url

from source.items import ProductItem


class CultbeautySpider(CrawlSpider):
    name = "cultbeauty"
    custom_settings = {"IMAGES_STORE": '../images/cultbeauty'}

    allowed_domains = ["www.cultbeauty.co.uk"]
    start_urls = [
        'https://www.cultbeauty.co.uk/skin-care.html?ref=mm',
        'https://www.cultbeauty.co.uk/make-up.html?ref=mm',
        'https://www.cultbeauty.co.uk/fragrance.html?ref=mm',
        'https://www.cultbeauty.co.uk/hair-care.html?ref=mm',
        'https://www.cultbeauty.co.uk/bath-body.html?ref=mm',
        'https://www.cultbeauty.co.uk/wellbeing.html?ref=mm',
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
        all_ull = response.xpath(
            '//ul[@class="refineItemOptions"]')
        links = all_ull[0].xpath('./li/a/@href')
        all_links = []
        for link in links:
            if link.extract() == '/':
                print("contineued")
                continue
            import urlparse
            full_url = urlparse.urljoin(response.url, link.extract())
            print("full url", full_url)
            all_links.append(scrapy.Request(
                full_url,
                self.parse_items))
        return all_links

    def parse_items(self, response):
        print("---------------------------------------------")
        print(response.url)
        print("---------------------------------------------")
        sub_category = response.xpath('//title/text()').extract_first()
        category_org = response.xpath('//div[@class="breadcrumb"]/ol/li')
        print(category_org)
        category = category_org[1].xpath('./a/span/text()').extract_first()
        mobile_items = response.xpath('//div[@class="productGridItem"]')
        # file_ = open('Failed.html', 'w')
        # file_.write(response.body)
        # file_.close()
        for mobile_item in mobile_items:
            try:
                image_urls = "http:" + mobile_item.xpath('.//img/@data-src').extract_first()
            except:
                image_urls = "http:" + mobile_item.xpath('.//img/@src').extract_first()

            image_urls = [str(image_urls)]
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
                image_urls=image_urls,
                brand=brand.strip(),
                affiliate_link=affiliate_link,
                category=category,
                sub_category=sub_category,
                website=website
            )
            yield item
