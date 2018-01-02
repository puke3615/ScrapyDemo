import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    n_pages = 3
    start_urls = ['http://quotes.toscrape.com/page/%d/' % i for i in range(1, n_pages + 1)]

    def parse(self, response):
        page = response.url.split('/')[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
