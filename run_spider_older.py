from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from source.spiders.beautybay_spider import BeautybaySpider
from source.spiders.beautylish_spider import BeautyLishSpider
from source.spiders.cultbeauty_spider import CultbeautySpider
from source.spiders.mac_spider import MacSpider
from source.spiders.maybelline_spider import MaybellineSpider
from source.spiders.netaporter_spider import NetaporterSpider
from source.spiders.polyvore_spider import PolyvoreSpider
from source.spiders.selfridges_spider import SelfridgesSpider
from source.spiders.sephora_spider import SephoraSpider
from source.spiders.shopstyle_spider import ShopStyleSpider


configure_logging()
runner = CrawlerRunner()


@defer.inlineCallbacks
def crawl():
    yield runner.crawl(BeautybaySpider)
    yield runner.crawl(BeautyLishSpider)
    yield runner.crawl(CultbeautySpider)
    yield runner.crawl(MacSpider)
    yield runner.crawl(MaybellineSpider)
    yield runner.crawl(NetaporterSpider)
    yield runner.crawl(PolyvoreSpider)
    yield runner.crawl(SelfridgesSpider)
    yield runner.crawl(SephoraSpider)
    yield runner.crawl(SephoraSpider)
    reactor.stop(ShopStyleSpider)

crawl()
reactor.run()  # the script will block here until the last crawl call is finished
