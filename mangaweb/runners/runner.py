"""Requests to pull info from manga sites. Using get"""
import time
from mangaweb.Retriever.Retriever import BookCreator, SeriesCreator

# print(BookCreator.getProduct('https://www.python.org/doc/#'))
# print(BookCreator.get_product('https://booklive.jp/product/index/title_id/1000/'))
# time.sleep(5)

try:
    book = BookCreator.get_product('https://booklive.jp/product/index/title_id/1000/')
    print(book)

    time.sleep(2)

    series = SeriesCreator.get_series('https://booklive.jp/product/index/title_id/1000/')
    print(series)
except Exception as e:
    print(e)
