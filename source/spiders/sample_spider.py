from scrapy.spider import BaseSpider
# from scrapy.http import Request

class SeleniumSprider(BaseSpider):
    name = "sample"
    # allowed_domains = ['beautybay']
    start_urls = [
        "http://jobsearch.monster.co.uk/jobs/?q=python&where=london&cy=uk",
        "http://jobsearch.monster.co.uk/jobs/?q=python&where=london&cy=uk",
        "http://jobsearch.monster.co.uk/jobs/?q=python&where=london&cy=uk",
        "http://jobsearch.monster.co.uk/jobs/?q=python&where=london&cy=uk",
        "http://jobsearch.monster.co.uk/jobs/?q=python&where=london&cy=uk",
        "http://jobsearch.monster.co.uk/jobs/?q=python&where=london&cy=uk",
        "http://jobsearch.monster.co.uk/jobs/?q=python&where=london&cy=uk",
        "http://jobsearch.monster.co.uk/jobs/?q=python&where=london&cy=uk",
        "http://jobsearch.monster.co.uk/jobs/?q=python&where=london&cy=uk",
        "http://jobsearch.monster.co.uk/jobs/?q=python&where=london&cy=uk",
        "http://jobsearch.monster.co.uk/jobs/?q=python&where=london&cy=uk",
        "http://jobsearch.monster.co.uk/jobs/?q=python&where=london&cy=uk",
        "http://jobsearch.monster.co.uk/jobs/?q=python&where=london&cy=uk",
        "http://jobsearch.monster.co.uk/jobs/?q=python&where=london&cy=uk",
        "http://jobsearch.monster.co.uk/jobs/?q=python&where=london&cy=uk",
        "http://jobsearch.monster.co.uk/jobs/?q=python&where=london&cy=uk",
        "http://jobsearch.monster.co.uk/jobs/?q=python&where=london&cy=uk",
        "http://jobsearch.monster.co.uk/jobs/?q=python&where=london&cy=uk",
        "http://jobsearch.monster.co.uk/jobs/?q=python&where=london&cy=uk",
        "http://jobsearch.monster.co.uk/jobs/?q=python&where=london&cy=uk",
        "http://jobsearch.monster.co.uk/jobs/?q=python&where=london&cy=uk",
        "http://jobsearch.monster.co.uk/jobs/?q=python&where=london&cy=uk",
        "http://jobsearch.monster.co.uk/jobs/?q=python&where=london&cy=uk",
        "http://jobsearch.monster.co.uk/jobs/?q=python&where=london&cy=uk",
        "http://jobsearch.monster.co.uk/jobs/?q=python&where=london&cy=uk",
        ]

    def parse(self, response):
        print ("--------------")
        print(response)
        # sel.open("/index.aspx")
        # sel.click("id=radioButton1")
        # sel.select("genderOpt", "value=male")
        # sel.type("nameTxt", "irfani")
        # sel.click("link=Submit")
        # time.sleep(1) #wait a second for page to load
        # root = lxml.html.fromstring(sel.get_html_source())