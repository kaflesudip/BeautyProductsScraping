# Beautyscraper #


### Scraping top 10 beauty e-commerce sites. ###

Scrape 10 sites as listed by the client.


### How do I get set up? ###

* ` pip install requirements.txt`
* `scrapy crawl <site_name> `

## Example of scraping:

`scrapy crawl sephora -o sephora.json`


### List of sites to crawl ###

* maccosmetics.com
* beautybay.com
* cultbeauty.co.uk
* sephora.com
* maybelline.co.uk
* selfridges.com
* Polyvore.com
* net-a-porter.com
* shopstyle.co.uk
* beautylish.com


### Libraries used:

The project runs on Python 2.7.

	1. Scrapy
	2. Pillow for saving images.
	3. scrapy-fake-useragent for rotating browser headers.