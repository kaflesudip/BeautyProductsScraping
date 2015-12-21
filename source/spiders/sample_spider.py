from selenium import webdriver
from scrapy.spider import BaseSpider
# from scrapy.http import Request
import time
import lxml.html

class SeleniumSprider(BaseSpider):
    name = "sample"
    allowed_domains = ['beautybay']
    start_urls = ["http://www.beautybay.com/cosmetics/_/N-23Z1xZ1wZ1vZ1uZ1tZo/"]

    def __init__(self, **kwargs):
        print kwargs
        self.driver = webdriver.PhantomJS()

    def parse(self, response):
        print ("--------------")
        new_response = self.driver.get(response.url)
        print(new_response)
        # sel.open("/index.aspx")
        # sel.click("id=radioButton1")
        # sel.select("genderOpt", "value=male")
        # sel.type("nameTxt", "irfani")
        # sel.click("link=Submit")
        # time.sleep(1) #wait a second for page to load
        # root = lxml.html.fromstring(sel.get_html_source())