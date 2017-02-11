'''
A simple scrapy spider to scrap XKCD.
'''

from urllib2 import urlopen
import scrapy

class XKCDSpider(scrapy.Spider):
    '''Scrap XKCD.'''

    name = 'XKCD'
    start_urls = ['https://xkcd.com/1/']

    def parse(self, resp):
        '''Grab the images from XKCD.'''

        try:
            # messy solution to a messy problem (in ways of Shakespeare: Violent delights have violent ends)
            url = 'http://' + resp.xpath('//div[@id="comic"]/img').xpath('@src').extract()[0][2:]

            img_name = url.rpartition('/')[-1]
            imgdata = urlopen(url).read()
            open(img_name, 'wb').write(imgdata)
        except Exception:
            # there is a problem with page 191, we skip that page
            pass
        finally:
            # in case you think this is ugly: eyes holdeth beauty
            next_pg = resp.css('ul.comicNav').xpath('//li/a').xpath('@href').extract()[-2]
            if next_pg:
                next_pg = resp.urljoin(next_pg)
                yield scrapy.Request(next_pg, callback=self.parse)
