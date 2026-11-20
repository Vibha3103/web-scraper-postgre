import scrapy
from books.items import BooksItem


class BookSpider(scrapy.Spider):

    name = "book"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):

        books = response.css("article.product_pod")

        for book in books:
            item = BooksItem()
            item['title'] = book.css("h3 > a::attr(title)").get()

            price=book.css(".price_color::text").get()
            item['price'] = (float(price.replace("£", "").strip())
            if price else None)
            
            item['url'] = response.urljoin(book.css("h3 > a::attr(href)").get())

            yield item


#pagination
        next_page = response.css("li.next > a::attr(href)").get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

