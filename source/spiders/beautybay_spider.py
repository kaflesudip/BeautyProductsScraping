import scrapy
from scrapy.spiders import CrawlSpider
# from scrapy.utils.response import get_base_url

from source.items import ProductItem
import urllib


URLS_TO_CRAWL = {
    "Eyes": {
        "Eye Liner": "http://beautybay.com/cosmetics/Eye-Liner/_/N-1z140tmZo/",
        "Eye Primers": "http://beautybay.com/cosmetics/Eye-Primers/_/N-1z13djpZo/",
        "Eyebrow & Eyelash Treatments": "http://beautybay.com/cosmetics/Eyebrow-Eyelash-Treatments/_/N-1z00n4jZo/",
        "Eyebrow Colour & Shaping": "http://beautybay.com/cosmetics/Eyebrow-Colour-Shaping/_/N-1z00n49Zo/",
        "Eyeshadow": "http://beautybay.com/cosmetics/Eyeshadow/_/N-1z140thZo/",
    },

    "Face": {
        "Face Primers": "http://beautybay.com/cosmetics/Face-Primers/_/N-1z13djyZo/",
        "False Eyelashes & Glue": "http://beautybay.com/cosmetics/False-Eyelashes-Glue/_/N-1z00mvjZo/",
        "Finishing": "http://beautybay.com/cosmetics/Finishing/_/N-1z140tqZo/",
        "Foundation": "http://beautybay.com/cosmetics/Foundation/_/N-1z140tiZo/",
        "Highlighters": "http://beautybay.com/cosmetics/Highlighters/_/N-1z00n4bZo/",
    },

    "Lips": {
        "Lip & Cheek Tints": "http://beautybay.com/cosmetics/Lip-Cheek-Tints/_/N-1z00n47Zo/",
        "Lip Balms": "http://beautybay.com/cosmetics/Lip-Balms/_/N-1z13djvZo/",
        "Lip Pencils": "http://beautybay.com/cosmetics/Lip-Pencils/_/N-1z13djlZo/",
        "Lip Plumpers": "http://beautybay.com/cosmetics/Lip-Plumpers/_/N-1z13djoZo/",
        "Lip Primer": "http://beautybay.com/cosmetics/Lip-Primer/_/N-1z13eydZo/",
        "Lipgloss": "http://beautybay.com/cosmetics/Lipgloss/_/N-1z140yhZo/",
        "Lipsticks": "http://beautybay.com/cosmetics/Lipsticks/_/N-1z13djmZo/",
    },
    "Makeup": {
        "Makeup Bags & Storage": "http://beautybay.com/cosmetics/Makeup-Bags-Storage/_/N-1z00kwgZo/",
        "Makeup Brush Sets": "http://beautybay.com/cosmetics/Makeup-Brush-Sets/_/N-1z00l89Zo/",
        "Makeup Brushes": "http://beautybay.com/cosmetics/Makeup-Brushes/_/N-1z00kwkZo/",
        "Makeup Remover": "http://beautybay.com/cosmetics/Makeup-Remover/_/N-1z00kwmZo/",
        "Mascara": "http://beautybay.com/cosmetics/Mascara/_/N-1z140yaZo/",
        "Palettes": "http://beautybay.com/cosmetics/Palettes/_/N-1z13djnZo/",
        "Powders": "http://beautybay.com/cosmetics/Powders/_/N-1z13djsZo/",
        "Sets": "http://beautybay.com/cosmetics/Sets/_/N-1z00n64Zo/",
        "Special Effects": "http://beautybay.com/cosmetics/Special-Effects/_/N-1z0vannZo/",
        "Strobing": "http://beautybay.com/cosmetics/Strobing/_/N-1z00kqvZo/",
    },

    "Skin": {
        "Sun Care": "http://beautybay.com/cosmetics/Sun-Care/_/N-1z14073Zo/",
        "Tinted Moisturisers": "http://beautybay.com/cosmetics/Tinted-Moisturisers/_/N-1z13djiZo/",
        "Toners": "http://beautybay.com/cosmetics/Toners/_/N-1z13dk4Zo/",
        "Treatments": "http://beautybay.com/cosmetics/Treatments/_/N-1z13dk5Zo/",
    },

    "Skincare": {
        "BB & CC Creams": "http://beautybay.com/skincare/BB-CC-Creams/_/N-1z00n45Zm/",
        "Cleansers": "http://beautybay.com/skincare/cleansers/_/N-1z13dk0Zm/",
        "Exfoliators": "http://beautybay.com/skincare/exfoliators/_/N-1z13dk3Zm/",
        "Eye Care": "http://beautybay.com/skincare/eye-care/_/N-1z140hlZm/",
        "Eye Masks": "http://beautybay.com/skincare/eye-masks/_/N-1z00n4hZm/",
        "Eyebrow & Eyelash Treatments": "http://beautybay.com/skincare/Eyebrow-Eyelash-Treatments/_/N-1z00n4jZm/",
        "Face Masks": "http://beautybay.com/skincare/face-masks/_/N-1z00n4lZm/",
        "Hair Removal": "http://beautybay.com/skincare/hair-removal/_/N-1z140guZm/",
        "Lip Balms": "http://beautybay.com/skincare/Lip-Balms/_/N-1z13djvZm/",
        "Lipgloss": "http://beautybay.com/skincare/Lipgloss/_/N-1z140yhZm/",
        "Makeup Remover": "http://beautybay.com/skincare/Makeup-Remover/_/N-1z00kwmZm/",
        "Moisturisers": "http://beautybay.com/skincare/moisturisers/_/N-1z13dk1Zm/",
        "Night Creams": "http://beautybay.com/skincare/night-creams/_/N-1z13djzZm/",
        "Self Tan": "http://beautybay.com/skincare/self-tan/_/N-1z140y8Zm/",
        "Serum": "http://beautybay.com/skincare/serum/_/N-1z0smvmZm/",
        "Sets": "http://beautybay.com/skincare/Sets/_/N-1z00n64Zm/",
        "Sun Care": "http://beautybay.com/skincare/Sun-Care/_/N-1z14073Zm/",
        "Supplements": "http://beautybay.com/skincare/supplements/_/N-1z140izZm/",
        "Tinted Moisturisers": "http://beautybay.com/skincare/Tinted-Moisturisers/_/N-1z13djiZm/",
        "Toners": "http://beautybay.com/skincare/Toners/_/N-1z13dk4Zm/",
        "Treatments": "http://beautybay.com/skincare/Treatments/_/N-1z13dk5Zm/",

    },

    "Bath and Body": {
        "Bath": "http://beautybay.com/bathandbody/_/N-1z13ehzZp/",
        "Bath Accessories": "http://beautybay.com/bathandbody/bath-accessories/_/N-1z00l98Zp/",
        "Body Makeup": "http://beautybay.com/bathandbody/Body-Makeup/_/N-1z00kwcZp/",
        "Body Oil": "http://beautybay.com/bathandbody/body-oil/_/N-1z14072Zp/",
        "Body Wash": "http://beautybay.com/bathandbody/body-wash/_/N-1z13ew8Zp/",
        "Deodorant": "http://beautybay.com/bathandbody/deodorant/_/N-1z140giZp/",
        "Exfoliators": "http://beautybay.com/bathandbody/exfoliators/_/N-1z13dk3Zp/",
        "Firming & Toning": "http://beautybay.com/bathandbody/firming-toning/_/N-1z00l7iZp/",
        "Foot Care": "http://beautybay.com/bathandbody/foot-care/_/N-1z14083Zp/",
        "Fragrances": "http://beautybay.com/bathandbody/fragrances/_/N-1z13d73Zp/",
        "Gift Sets & Kits": "http://beautybay.com/bathandbody/gift-sets-kits/_/N-1z1407eZp/",
        "Hair Removal": "http://beautybay.com/bathandbody/hair-removal/_/N-1z140guZp/",
        "Hand Wash & Care": "http://beautybay.com/bathandbody/hand-wash-care/_/N-1z00l94Zp/",
        "Highlighters": "http://beautybay.com/bathandbody/Highlighters/_/N-1z00n4bZp/",
        "Home Fragrance": "http://beautybay.com/bathandbody/home-fragrance/_/N-1z00l96Zp/",
        "Moisturisers": "http://beautybay.com/bathandbody/moisturisers/_/N-1z13dk1Zp/",
        "Powders": "http://beautybay.com/bathandbody/Powders/_/N-1z13djsZp/",
        "Self Tan": "http://beautybay.com/bathandbody/self-tan/_/N-1z140y8Zp/",
        "Sets": "http://beautybay.com/bathandbody/Sets/_/N-1z00n64Zp/",
        "Shampoo": "http://beautybay.com/bathandbody/shampoo/_/N-1z140ygZp/",
        "Soap": "http://beautybay.com/bathandbody/soap/_/N-1z140f6Zp/",
        "Sun Care": "http://beautybay.com/bathandbody/Sun-Care/_/N-1z14073Zp/",
        "Supplements": "http://beautybay.com/bathandbody/supplements/_/N-1z140izZp/",
        "Treatments": "http://beautybay.com/bathandbody/Treatments/_/N-1z13dk5Zp/",
    },

    "Haircare": {
        "Conditioners": "http://beautybay.com/haircare/conditioners/_/N-1z13dk6Zk/",
        "Curl Definer": "http://beautybay.com/haircare/curl-definer/_/N-1z13egcZk/",
        "Curling Tongs": "http://beautybay.com/haircare/curling-tongs/_/N-1z00mvpZk/",
        "Detangler": "http://beautybay.com/haircare/detangler/_/N-1z13eywZk/",
        "Finishing": "http://beautybay.com/haircare/Finishing/_/N-1z140tqZk/",
        "Gel": "http://beautybay.com/haircare/gel/_/N-1z13eu5Zk/",
        "Hair Accessories": "http://beautybay.com/haircare/hair-accessories/_/N-1z13efzZk/",
        "Hair Brushes": "http://beautybay.com/haircare/hair-brushes/_/N-1z0ik0bZk/",
        "Hair Colour": "http://beautybay.com/haircare/hair-colour/_/N-1z0cmoyZk/",
        "Hair Masks": "http://beautybay.com/haircare/hair-masks/_/N-1z00n4fZk/",
        "Hair Oil": "http://beautybay.com/haircare/hair-oil/_/N-1z13eyzZk/",
        "Hairspray": "http://beautybay.com/haircare/hairspray/_/N-1z140ieZk/",
        "Heat Protectors": "http://beautybay.com/haircare/heat-protectors/_/N-1z00n60Zk/",
        "Masks": "http://beautybay.com/haircare/masks/_/N-1z13dk2Zk/",
        "Mousse": "http://beautybay.com/haircare/mousse/_/N-1z13eu8Zk/",
        "Salt Spray": "http://beautybay.com/haircare/salt-spray/_/N-1z13eu7Zk/",
        "Sets": "http://beautybay.com/haircare/Sets/_/N-1z00n64Zk/",
        "Shampoo": "http://beautybay.com/haircare/shampoo/_/N-1z140ygZk/",
        "Shine Enhancer": "http://beautybay.com/haircare/shine-enhancer/_/N-1z13egiZk/",
        "Sun Care": "http://beautybay.com/haircare/Sun-Care/_/N-1z14073Zk/",
        "Supplements": "http://beautybay.com/haircare/supplements/_/N-1z140izZk/",
        "Texturiser": "http://beautybay.com/haircare/texturiser/_/N-1z13ejfZk/",
        "Treatments": "http://beautybay.com/haircare/Treatments/_/N-1z13dk5Zk/",
        "Volumiser": "http://beautybay.com/haircare/volumiser/_/N-1z13eg1Zk/",
        "Wax": "http://beautybay.com/haircare/wax/_/N-1z0rgltZk/",
    },

    "Nails": {
        "Beauty Tools": "http://beautybay.com/nailcare/Beauty-Tools/_/N-1z00l9aZr/",
        "Cuticle Care": "http://beautybay.com/nailcare/cuticle-care/_/N-1z140ykZr/",
        "Hand Wash & Care": "http://beautybay.com/nailcare/hand-wash-care/_/N-1z00l94Zr/",
        "Nail Files & Tools": "http://beautybay.com/nailcare/nail-files-tools/_/N-1z00mvbZr/",
        "Nail Treatments": "http://beautybay.com/nailcare/nail-treatments/_/N-1z00n3xZr/",
        "Scissors & Clippers": "http://beautybay.com/nailcare/scissors-clippers/_/N-1z13cmyZr/",
        "Sets": "http://beautybay.com/nailcare/Sets/_/N-1z00n64Zr/",
        "Supplements": "http://beautybay.com/nailcare/supplements/_/N-1z140izZr/",
        "Top Coat & Finishing": "http://beautybay.com/nailcare/top-coat-finishing/_/N-1z00n3zZr/",
    }
}

google_cache_link = "http://webcache.googleusercontent.com/search?q=cache%3A{0}&oq=cache%3A&ie=UTF-8&aqs=chrome.2.69i57j69i58j69i59l3j69i60.5737j0j4&sourceid=chrome-instant&ion=1&bav=on.2,or.r_cp.&bvm=bv.110151844,d.c2E&biw=1366&bih=680&dpr=1&ech=1&psi=JDuJVoSWOdGQuAT-5ICADA.1451834150635.3&ei=JDuJVoSWOdGQuAT-5ICADA&emsg=NCSR&noj=1"


class BeautybaySpider(CrawlSpider):
    name = "beautybay"
    custom_settings = {
        "IMAGES_STORE": '../images/beautybay',
        "DOWNLOAD_DELAY": 5,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "RANDOMIZE_DOWNLOAD_DELAY": True,
        "COOKIES_ENABLED": True
    }

    # allowed_domains = ["maybelline.co.uk"]
    start_urls = [
        'http://facebook.com'
    ]

    def parse_start_url(self, response):
        all_links = []
        for category, sub_categories in URLS_TO_CRAWL.iteritems():
            for sub_category, link in sub_categories.iteritems():
                full_url = google_cache_link.format(urllib.quote(link))
                my_request = scrapy.Request(
                    full_url,
                    self.parse_items)
                my_request.meta['category'] = {
                    "sub_category": sub_category,
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
        products = response.xpath('//div[contains(@class, "product needsclick")]')
        for each_item in products:
            name = each_item.xpath('.//p[@class="description"]/text()').extract_first()
            print(name)
            brand = each_item.xpath('.//p[@class="brand"]/text()').extract_first()
            price = each_item.xpath('.//p[@class="pricing"]/text()').extract_first()
            affiliate_link = "http://beautybay.com" + each_item.xpath('./a/@href').extract_first()
            website = "beautybay.com"
            image_urls = [
                "http:" + response.xpath(".//img/@data-src").extract_first()]
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
        next_page = response.xpath("//a[@id='next-page']/@href").extract_first()
        print "next page", next_page
        if next_page:
            url = "http://beautybay.com" + next_page
            full_url = google_cache_link.format(url)
            new_request = scrapy.Request(full_url, self.parse_items)
            new_request.meta['category'] = response.meta['category']
            yield new_request
