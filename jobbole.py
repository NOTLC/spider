# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import re
from ArticleSpider.items import ArticleItem
from scrapy.loader import ItemLoader
from urllib import parse

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobble.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        #解析列表中的所有文章url并交给scrapy下载后并进行解析
        post_urls = response.xpath('//span[@class="read-more"]/a/@href').extract()
        for post_url in post_urls:
            yield Request(url = post_url,callback=self.parse_detail,dont_filter=True)##这里直接是url了，有些网站前面是没有域名的
            #我们只需要这样做
            '''
            parse需要导包from urllib import parse
            urljoin（）这个函数就是拼接url的，域名加上不完整的url，就算url是完整的，也是没有影响的
            request(url=parse.urljoin(response.url,post_url),callback=回调函数名称)
            '''
        #获取下一页url，如果有存在的话就回调给我们parse函数
        page_url = response.xpath('//a[@class="next page-numbers"]/@href').extract()[0]
        if page_url:
            yield Request(url=page_url, callback=self.parse, dont_filter=True)
            # print(post_url)
    def parse_detail(self,response):
        #提取文章中的具体字段
        #实例化item
        ArticleItems = ArticleItem()
        pages = response
        ArticleItems['urll'] = re.split(" |<|>",str(pages))[-2]
        munb = str(pages).split('/')[-2]
        htmls = response.xpath('//div[@id="post-%d"]'%int(munb))
        #标题
        ArticleItems['title'] = htmls.xpath('./div[@class = "entry-header"]/h1/text()').extract()[0]
        #创建时间
        ArticleItems['create_date'] = htmls.xpath('./div[@class = "entry-meta"]/p/text()').extract()[0].strip().split(' ')[0]
        #点赞
        try:
            ArticleItems['praise_num'] = htmls.xpath('//h10[@id="%dvotetotal"]/text()'%int(munb)).extract()[0]
        except:
            praise_num = 0
        #收藏数
        ArticleItems['fav_nums'] = htmls.xpath('//span[@data-item-id="%d"]/text()'%int(munb)).extract()[0]
        #评论数
        ArticleItems['comment_nums'] = htmls.xpath('//span[@class="btn-bluet-bigger href-style hide-on-480"]/text()').extract()[0]
        #职场
        ArticleItems['job_market'] = htmls.xpath('./div[@class = "entry-meta"]/p/a/text()').extract()[0]
        #类型
        try:
            ArticleItems['genre'] = htmls.xpath('./div[@class = "entry-meta"]/p/a/text()').extract()[1]
        except:
            ArticleItems['genre'] = None
        # print(page)
        # print(title,create_date,praise_num,fav_nums,comment_nums,job_market,genre)
        yield ArticleItems


'''

如果需要下载当前url列表中的封面图的话可以在#解析列表中的所有文章url并交给scrapy下载后并进行解析这里代码换一换
比如有一个节点包含着url和封面图的url的话可以这样做
post_node = response.xpath('//span[@class="read-more"]')#获取节点
        for post_node in post_nodes:
            post_url = post_node.xpath('获取具体的url')
            post_img = post_node.xpath()
            yield Request(url=parse.urljoin(response.url,post_url),meta={"post_img" = post_img},callback=self.parse_detail,dont_filter=True)




'''
