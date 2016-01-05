import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
import urllib2
import json


# from scrapy.utils.response import get_base_url

from source.items import ProductItem


class ShopStyleSpider(CrawlSpider):
    name = "shopstyle"
    custom_settings = {"IMAGES_STORE": '../images/shopstyle'}

    allowed_domains = ["www.shopstyle.co.uk"]
    start_urls = [
        # 'http://www.shopstyle.co.uk',
        'http://www.shopstyle.co.uk/browse/womens-beauty',

    ]


    def parse_start_url(self, response):
        product_dict = {}
        product_dict['body-cleansers'] = ['bath-shower-gel', 'bubble-bath-bath-oil', 'body-cleansers-soap', 'deodorant', 'shave-cream']
        product_dict['body-moisturizers'] = ['body-lotions-creams', 'body-oils']
        product_dict['body-treatments'] = ['all-over-body-treatments', 'body-scrubs-exfoliants', 'cellulite-treatments', 'neck-decollete', 'hand-treatments', 'foot-leg-treatments']
        product_dict['tooth-care'] = ['tooth-whiteners', 'toothpaste']
        product_dict['bath-body'] = ['bath-body-gift-sets']
        product_dict['womens-beauty'] = ['perfume', 'hair-accessories']
        product_dict['hair-care'] = ['hair-conditioner', 'hair-styling-tools', 'hair-scalp-treatments','hair-shampoo', 'hair-styling-products']
        product_dict['beauty-body-makeup'] = ['body-shimmer-glitter', 'body-makeup']
        product_dict['eye-makeup'] = ['eye-shadow', 'eyes-shimmer-glitter', 'eyeliner', 'mascara', 'false-eyelashes', 'eyebrow-enhancers', 'eyes-concealer-shadow-base','eye-makeup-remover']
        product_dict['face-makeup'] = ['blush', 'face-primer', 'face-concealer', 'face-liquid-foundation', 'face-cream-foundation', 'face-powder-foundation', 'face-loose-powder', 'face-pressed-powder', 'face-shine-control-blotting-papers', 'face-bronzer', 'face-luminizer', 'face-shimmer-glitter']
        product_dict['lip-products'] = ['lip-gloss', 'lip-plumpers', 'lipstick', 'lip-stain', 'lip-pencils', 'lip-treatments']
        product_dict['nail-products'] = ['nail-treatments', 'nail-polish']
        product_dict['makeup'] = ['makeup-sets']
        product_dict['eye-care'] = ['eyes-fine-lines-wrinkles', 'eyes-dryness', 'eyes-dark-circles', 'eyes-puffiness', 'eye-treatments']
        product_dict['face-care'] = ['face-makeup-removers', 'face-cleansers', 'face-toners', 'face-moisturizers', 'face-tinted-moisturizers', 'lip-balm-treatments', 'face-anti-aging', 'face-oil-blemish-control', 'face-scrubs-exfoliants', 'face-masks', 'face-skin-revitalizers', 'face-skin-lighteners', 'face-night-treatments']
        product_dict['sun-care'] = ['spf-15-below', 'spf-15-above', 'sun-water-resistant', 'after-sun', 'sun-bronzers-self-tanners']
        product_dict['beauty-tools-bags-cases'] = ['makeup-travel-bags', 'bags-cases-brush-bags', 'bags-cases-train-cases', 'bags-cases-refillables']
        product_dict['beauty-tools-brushes-applicators'] = ['brushes-applicators-face', 'brushes-applicators-eyes', 'brushes-applicators-lips', 'brushes-applicators-sets', 'brushes-applicators-cleaners']
        product_dict['beauty-tools'] = ['beauty-tools-eyelash-curler', 'eauty-tools-foot-tools', 'beauty-tools-hair-removal', 'beauty-tools-nail-tools', 'beauty-tools-mirrors', 'beauty-tools-scissors-shears']
       
        for key, value in product_dict.iteritems():
            for each_value in value:
                my_url = 'http://www.shopstyle.co.uk/api/v2/site/search?device=desktop&includeCategoryHistogram=true&includeProducts=true&limit=40&locales=all&pid=shopstyle&prevCat=women&productScore=LessPopularityEPC&url=%2Fbrowse%2F'+each_value+'&view=angular'
                print "my_url", my_url
                my_response = urllib2.urlopen(my_url)
                my_data = json.load(my_response)
                # print "my_product", my_data['products']
                category_list = key.split('-')
                category = " ".join(category_list).upper()
                sub_category_list = each_value.split('-')
                sub_category = " ".join(sub_category_list).upper()
                website = "http://www.shopstyle.co.uk/"
                my_data_product = my_data['products']
                print "my_data_product", len(my_data_product)
                print "type ", type(my_data_product)
                for each_product in my_data_product:

                    name = each_product.get('name')
                    price = each_product.get('price')
                    if each_product.get('brand'):
                        brand = each_product.get('brand').get('name')
                    else:
                        brand = None
                    affiliate_link = each_product.get('clickUrl')
                    website = website
                    image_urls = [str(each_product.get('image').get('sizes').get('Best').get('url'))]
                    item = ProductItem(
                        name=name.strip(),
                        price=price,
                        image_urls=image_urls,
                        brand=brand,
                        affiliate_link=affiliate_link,
                        category=category,
                        sub_category=sub_category,
                        website=website
                    )
                    yield item
