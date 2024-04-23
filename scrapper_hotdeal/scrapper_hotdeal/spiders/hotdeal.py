from typing import Any
import scrapy


class HotdealSpider(scrapy.Spider):
    name = "hotdeal"
    allowed_domains = ["www.fmkorea.com"]
    start_urls = ["https://www.fmkorea.com/index.php?mid=hotdeal"]

    def __init__(self):
        self.page_num = 1
    

    def parse(self, response):
        headers_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'AppleWebKit/537.36 (KHTML, like Gecko)', 'Chrome/123.0.0.0', 'Safari/537.36']
        headers = {'user-agent': headers_list[0]}
        # items = []
        for i in range(1, 21):
            item = {}
            deal = scrapy.Selector(text=response.xpath(f'//*[@id="bd_1196365581_0"]/div/div[3]/ul/li[{i}]').get())
            # deal = response.xpath(f'//*[@id="bd_1196365581_0"]/div/div[3]/ul/li[{i}]').get()
            item['title'] = deal.xpath('..//div[@class="li"]/h3[@class="title"]/a[@class=" hotdeal_var8"]/text()').get()
            item['category'] = deal.xpath('..//div[@class="li"]/div/span[@class="category"]/a/text()').get()
            item['register_time'] = deal.xpath('..//div[@class="li"]/div/span[@class="regdate"]/text()').get()
            item['info'] = deal.xpath('..//div[@class="li"]/div[@class="hotdeal_info"]/span/a/text()').getall()
            item['url'] = 'https://www.fmkorea.com' + deal.xpath('..//div[@class="li"]/h3[@class="title"]/a/@href').get()
            if len(item['register_time']) >= 10:
                self.logger.info(f"register_time length is greater than or equal to 10: {item['register_time']}")
                raise scrapy.exceptions.CloseSpider(reason='register_time length is greater than or equal to 10')  # 스크래핑 완전히 중단
            else:
                yield item
        self.page_num += 1
        next_page_url = f"https://www.fmkorea.com/index.php?mid=hotdeal&page={self.page_num}"  # 다음 페이지의 URL 생성
        yield scrapy.Request(next_page_url, callback=self.parse)
            # print(len(item['register_time']))
        #     items.append(item)
        # yield items

        