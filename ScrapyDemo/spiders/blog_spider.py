from scrapy.selector import Selector
import scrapy


class BlogSpider(scrapy.Spider):
    name = 'blog'
    start_urls = [
        'https://puke3615.github.io/',
    ]
    page = 1

    def parse(self, response):
        data = response.xpath('/html/body/div/div/div[1]/div[*]').extract()

        filename = '%s.txt' % self.name
        with open(filename, 'a') as f:
            for item in data:
                selector = Selector(text=item)
                title = selector.xpath('//h4/text()').extract_first().encode('utf-8').strip()
                sub_title = selector.xpath('//div[@class="post-content-preview"]/text()').extract()[1].encode('utf-8').strip()
                time = selector.xpath('//p[@class="post-meta"]/text()').extract_first().encode('utf-8').strip()
                f.write('[title]: %s\n' % title)
                f.write('[sub_title]: %s\n' % sub_title)
                f.write('[time]: %s\n' % time)
                f.write('\n')
        self.page += 1
        yield scrapy.Request(self.get_url(), callback=self.parse)

    def get_url(self):
        if self.page == 1:
            return self.start_urls[0]
        else:
            return '%spage/%d/' % (self.start_urls[0], self.page)
