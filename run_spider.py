from twisted.internet import reactor
from scrapy.crawler import Crawler
# scrapy.conf.settings singlton was deprecated last year
from scrapy.utils.project import get_project_settings
from scrapy import log


def setup_crawler(spider_name):
    crawler = Crawler(settings)
    crawler.configure()
    spider = crawler.spiders.create(spider_name)
    crawler.crawl(spider)
    crawler.start()

# log.start()
settings = get_project_settings()
crawler = Crawler(settings)
crawler.configure()

for spider_name in crawler.spiders.list():
    setup_crawler(spider_name)

reactor.run()
