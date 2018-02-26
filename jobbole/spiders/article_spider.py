import scrapy
from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader
import time
import datetime
import re

from jobbole.items import JobBoleArticleItemLoader
from jobbole.items import JobboleItem

class article_spider(scrapy.Spider):
    name = "article_spider"
    allowed_domains = ['blog.jobbole.com/all-posts/']
    start_urls = ["http://blog.jobbole.com/all-posts/"]


    def parse(self, response):
        """
        #xpath way to get the urls and so on
        urls = response.xpath('//a[@class="archive-title"]/@href').extract()
        all_times = response.xpath('//div[@class="post-meta"]/p[1]/text()').extract()
        times = []
        for time in all_times:
            time = time.strip().replace(" ", "").strip()
            times.append(time)
        images = response.css(".post-thumb img::attr(src)").extract()
        """

        nodes = response.css("#archive .floated-thumb .post-thumb a")
        for node in nodes:
            image_url = node.css("img::attr(src)").extract_first()
            post_url = node.css("::attr(href)").extract_first()
            yield Request(url=parse.urljoin(response.url, post_url))


    def parse_detail(self, response):
        jobbole_item = JobboleItem()

        front_image_url = response.meta.get("front_image_url", "")
        item_loader = JobBoleArticleItemLoader(item=JobboleItem(), response=response)
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_value("url", response.url)
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_css("praise_nums", ".vote-post-up h10::text")
        item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
        item_loader.add_css("fav_nums", ".bookmark-btn::text")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("content", "div.entry")

        article_item = item_loader.load_item()

        yield article_item






