import re
import time
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor

class BookSpider(CrawlSpider):
    name = 'book'
    start_urls = ['http://www.quanwenyuedu.io/']

    # 每本书的开始url
    fisrt_link = LinkExtractor(allow=r'quanwenyuedu.io$', deny_domains=['big5.quanwenyuedu.io', 'www.quanwenyuedu.io'])
    # 开始阅读
    text_link = LinkExtractor(allow=r'/(\d+).html$')

    rules = (
        # 生成Rules对象，注意callback 的函数为 字符串
        Rule(fisrt_link, callback='get_book', follow=True),
        Rule(text_link, callback='get_ajax_info', follow=True),
    )
    # 进入小说入口
    def get_book(self, response):
        # print('get_book =========== ', response.url)
        # 拼音的小说名
        book_name = response.xpath('/html/body/h1/text()').extract()[0]
        # print(book_name)
        # 小说的基本信息
        book_info = '\n'.join(response.xpath('//div[@class="top"]/p//text()').extract())
        # print(book_name)
        # print(book_info)
        # 写入小说的基本信息
        with open(r'F:\Scrapy\books\book\\'+book_name+'.txt','a+') as  f:
            f.write(book_info + '\n\n\n')



    id = 1
    sky = 'c430514a75e0bf559a4185464b4bd4b1'
    t = 1510162912
    _type = 'ajax'
    rndval = 1510140808315

    # 先进行ajax请求
    def get_ajax_info(self, response):
        # 设置posrt请求的表数据
        from_data = {
            'a': 'ajax',
            'c': 'book',
        }
        # 设置正则的模版
        zz = re.compile(r'setTimeout.*')
        # 匹配全文
        js = zz.search(response.text)
        # 将匹配出的字符串用','分割
        js_list = js.group().split("','")
        from_data['id'] = js_list[3]
        from_data['sky'] = js_list[5]
        from_data['t'] = js_list[7].split("'")[0]
        from_data['rndval'] = str(int(time.time() * 1000))
        url_str = ''.join(response.url.split('io/')[:-1]) + 'io/index.php?c=book&a=ajax'

        yield scrapy.FormRequest(
            
        )

    # 找内容
    def get_text(self, response):
        book_name = response.url.split('.')[0].split('/')[-1]
        text_info = '\n'.join(response.xpath('.//div[@id="content"]/p//text()').extract() )
        print(text_info)
        # 这里还需要使用一次ajax请求，才能获取每章小说的全部内容
        with open(r'F:\Scrapy\books\book\\' + book_name + '.txt','a+') as  f:
            f.write(text_info + '\n\n\n')