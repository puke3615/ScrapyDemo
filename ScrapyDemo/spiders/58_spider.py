# coding=utf-8
from scrapy.selector import Selector
from threading import Lock
import scrapy


# http://hz.58.com/chuzu/?PGTID=0d100000-0004-fdce-fb70-93dab4917971&ClickID=1
# http://hz.58.com/chuzu/pn2/?PGTID=0d3090a7-0004-f536-9b28-d50a2639d96f&ClickID=2
# http://hz.58.com/chuzu/pn3/?PGTID=0d3090a7-0004-f3a5-9ff9-744cc5c5dbf7&ClickID=2


class _58Spider(scrapy.Spider):
    URL_TEMPLATE = 'http://hz.58.com/chuzu%s?PGTID=0d100000-0004-fdce-fb70-93dab4917971&ClickID=1'
    name = '58'
    start_urls = [URL_TEMPLATE % '']
    page = 1

    def parse(self, response):
        if response.status != 200:
            return
        data = response.xpath('/html/body/div[3]/div[1]/div[5]/div[2]/ul/li[*]').extract()
        filename = '%s.txt' % self.name
        with open(filename, 'a') as f:
            f.write('[page]: %d\n' % self.page)
            f.write('- ' * 30 + '\n')
            for item in data:
                # f.write(item.encode('utf-8').strip() + '\n\n')
                selector = Selector(text=item)

                title = selector.xpath('//div/h2/a/text()').extract_first()
                if title is not None:
                    title = title.encode('utf-8').strip()
                    f.write('[title]: %s\n' % title)

                # div[3]/div[2]/b
                price = selector.xpath('//div[*]/div[*]/b/text()').extract_first()
                if price is not None:
                    price = price.encode('utf-8').strip()
                    f.write('[price]: %s 元/月\n' % price)

                # div[2]/p[1]
                size = selector.xpath('//p[@class="room"]/text()').extract_first()
                if size is not None:
                    size = size.encode('utf-8').strip()
                    size_info = size.split(' ')
                    f.write('[type]: %s\n' % size_info[0].strip())
                    f.write('[size]: %s\n' % size_info[-1].strip())

                f.write('\n')

        self.page += 1
        yield scrapy.Request(self.get_url(), callback=self.parse)

    def get_url(self):
        if self.page == 1:
            return self.start_urls[0]
        else:
            page_str = '/pn%d' % self.page
            return self.URL_TEMPLATE % page_str
