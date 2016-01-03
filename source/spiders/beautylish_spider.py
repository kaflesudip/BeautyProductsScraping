import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector

# from scrapy.utils.response import get_base_url

from source.items import ProductItem


class BeautyLishSpider(CrawlSpider):
    name = "BeautyLish"
    allowed_domains = ["www.beautylish.com"]
    start_urls = [
        'http://www.beautylish.com',
        'https://www.beautylish.co.uk/make-up.html?ref=mm',
        'https://www.beautylish.co.uk/fragrance.html?ref=mm',
        'https://www.beautylish.co.uk/hair-care.html?ref=mm',
        'https://www.beautylish.co.uk/bath-body.html?ref=mm',
        'https://www.beautylish.co.uk/wellbeing.html?ref=mm',
    ]

    rules = [
        Rule(
            LxmlLinkExtractor(
                allow=(),
                deny=(),
                restrict_xpaths=(
                    '//li[@class="catMenu_expandable"][position()>1 and position()<=6]//li[contains(@class,"heading")]'
                )
            ),
            callback="parse_category",
            follow=True,
        )
    ]

    # def parse_start_url(self, response):
    #     print("entered")
    #     all_ull = response.xpath(
    #         '//div[contains(@class, "mb0")]/ul')
    #     # links = all_ull.xpath('./li/a/@href')
    #     print "all links", all_ull
        # all_links = []
        # for link in links:
        #     if link.extract() == '/':
        #         print("contineued")
        #         continue
        #     import urlparse
        #     full_url = urlparse.urljoin(response.url, link.extract())
        #     print("full url", full_url)
        #     all_links.append(scrapy.Request(
        #         full_url,
        #         self.parse_items))
        # return all_links

    def parse_category(self, response):
        # print "response", response.url, 'endresponse'
        sel = Selector(response)
        all_links = []
        if response.url == "http://www.beautylish.com/shop/browse?category=eye-makeup&ref=menu":
            extract_category = sel.xpath('//span[@class="filter_child_horizontal"]/descendant::text()').extract()[0]
            category = extract_category.split(':')[1].strip().replace('\n','').replace('\t','')
            data = sel.xpath('//div[contains(@class, "mb0")]/ul/li')
            for each in data:
                sub_category = each.xpath('.//a/text()').extract()
            links = data.xpath('./a/@href')
            for link in links:
                if link.extract() == '/':
                    print("contineued")
                    continue
                import urlparse
                full_url = urlparse.urljoin(response.url, link.extract())
                my_request = scrapy.Request(
                    full_url,
                    self.parse_items)
                my_request.meta['category'] = {
                    "sub_category": sub_category,
                    "category": category,
                    # "to_replace": "currentPage=1"
                }

                all_links.append(my_request)

        return all_links

    def parse_items(self, response):
        print "........................"
        print "entered items", response.url
        print "........................"
        # if response.url in (
        #     "http://www.beautylish.com/shop/browse?category=face-makeup",
        #     "http://www.beautylish.com/shop/browse?category=face-makeup&page=2",
        #     "http://www.beautylish.com/shop/browse?category=face-makeup&page=3"
        # ):

        items = response.xpath('//li[contains(@class,"browse")]')

        for each_item in items:
            try:
                image_urls = "http:" + each_item.xpath('.//img/@data-src').extract_first()
            except:
                image_urls = "http:" + each_item.xpath('.//img/@src').extract_first()

            image_urls = [str(image_urls)]
            brand = each_item.xpath('.//h6/text()').extract_first()
            name = each_item.xpath('.//h5/text()').extract_first()
            website = "http://www.beautylish.com"
            price = each_item.xpath('.//p//strong/text()').extract_first()
            affiliate_link = website + "/" + each_item.xpath('.//a/@href').extract_first()

            item = ProductItem(
                name=name.strip(),
                price=price.strip(),
                image_urls=image_urls,
                brand=brand.strip(),
                affiliate_link=affiliate_link,
                category=response.meta['category']['category'],
                sub_category=response.meta['category']['sub_category'][0],
                website=website
            )
            print item

        next_page = response.xpath("//div[@class='pager']/a/@href")
        print "next page", next_page
        if next_page:
            url = response.urljoin(next_page[0].extract())
            new_request = scrapy.Request(url, self.parse_items)
            new_request.meta['category'] = response.meta['category']
            yield new_request


