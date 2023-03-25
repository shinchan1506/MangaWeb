"""Requests to pull info from manga sites. Using get"""
from __future__ import annotations
from abc import abstractmethod
import datetime
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests

class Book():
    """
    genre: seinen manga
    category: shounen/seinen manga
    """
    def __init__(self, title, 
                 volume = 0, 
                 author = "None", 
                 series = "None", 
                 publisher = "None", 
                 published = datetime.datetime(1970, 1, 1), 
                 genre = "hentai", 
                 category = "hentai",
                 CoverArtUrl = ""
                 ) -> Book:
        self.title = title
        self.volume = volume
        self.author = author
        self.series = series
        self.publisher = publisher
        self.published = published
        self.genre = genre
        self.category = category
        self.coverArtUrl = CoverArtUrl
        pass

    def __str__(self) -> str:
        return ("Book: " + self.title + 
                " \nAuthor: " + self.author +
                " \nSeries: " + self.series +
                " \nPublisher: " + self.publisher +
                " \nPublished: " + self.published.strftime("%m/%d/%Y") +
                " \nGenre: " + self.genre + 
                " \nCategory: " + self.category +
                " \nCover Art URL: " + self.coverArtUrl)


class Retriever():
    
    @abstractmethod
    def getTitle(self, soup) -> str:
        pass

    @abstractmethod
    def getVolume(self, soup) -> str:
         pass
    
    @abstractmethod
    def getAuthor(self, soup) -> str:
        pass
    
    @abstractmethod
    def getSeries(self, soup) -> str:
        pass

    @abstractmethod
    def getPublisher(self, soup) -> str:
        pass

    @abstractmethod
    def getPublished(self, soup) -> datetime:
        pass

    @abstractmethod
    def getGenre(self, soup) -> str:
        pass

    @abstractmethod
    def getCategory(self, soup) -> str:
        pass

    @abstractmethod
    def getCoverArtUrl(self, soup) -> str:
        pass

    """
    Perform requests.get and encapsulate resulting html in Soup
    """
    def __getPageSoup(self, productUrl ) -> BeautifulSoup:
        req = requests.get( productUrl, timeout=240)
        soup = BeautifulSoup(req.content, 'html.parser')
        return soup

    def scrapeProduct(self, productUrl) -> Book:
        self.url = productUrl
        soup = self.__getPageSoup( productUrl )
        return Book(
            self.getTitle(soup),
            self.getVolume(soup),
            self.getAuthor(soup),
            self.getSeries(soup),
            self.getPublisher(soup),
            self.getPublished(soup),
            self.getGenre(soup),
            self.getCategory(soup),
            self.getCoverArtUrl(soup)
                    )

"""
Here is an example retriever to base your Retrievers off of.
"""
class ExampleRetriever(Retriever):
    def getTitle(self, soup) -> str:
        # select the text of the element that is class "call-to-action" that is nested in ele with class "documentation-banner" which is nested in ele w class "header-banner"
        title = soup.select_one('.header-banner .documentation-banner .call-to-action').text.strip()
        return title

    def getVolume(self, soup) -> str:
        volume = soup.select_one('.container .main-content .row .docs-by-version .widget-title').text.strip()
        return volume
    
    def getAuthor(self, soup) -> str:
        return "python"
    
    def getSeries(self, soup) -> str:
        return "python"

    def getPublisher(self, soup) -> str:
        return "python"

    def getPublished(self, soup) -> datetime:
        return datetime.datetime(1970, 1, 1)

    def getGenre(self, soup) -> str:
        return "python"

    def getCategory(self, soup) -> str:
        return "python"
    
    def getCoverArtUrl(self, soup) -> str:
        return "https://www.python.org/static/img/python-logo.png"

    """
    Get stuff from python
    """
    def scrapeProduct(self, productUrl) -> Book:
        book = super().scrapeProduct(productUrl)
        return book
    

class BookliveRetriever(Retriever):
    def getTitle(self, soup) -> str:
        title = soup.select_one(".product_info #product_display_1")
        if title: 
            return title.text.strip()
        return "NO TITLE"

    def getVolume(self, soup) -> str:
        # for booklive, volume number is consistently in url so extract from there
        matches = re.findall("(?<=vol_no/).*", self.url)
        if len(matches) > 0:
            return matches[0]
        return "-1"
    
    def getAuthor(self, soup) -> str:
        author = soup.select_one(".product_info .meta .author.clearfix .multiple_links a")
        if author: 
            return author.text.strip()
        return "NO AUTHOR"
    
    def getSeries(self, soup) -> str:
        series = soup.select_one(".detail_area.clearfix.ua_click .btn_subtitle h2")
        if series and len( re.findall(u"(.*?)\\xa0のシリーズ作品", series.text.strip()) ) > 0:
            return re.findall(u"(.*?)\\xa0のシリーズ作品", series.text.strip() )[0]
        return "NO SERIES"

    def getPublisher(self, soup) -> str:
        publisher = soup.select(".product_field.clearfix .product_specs .product_data.clearfix dd a")
        if len(publisher) > 3:
            return publisher[2].text.strip()
            
        return "booklive"

    def getPublished(self, soup) -> datetime:
        return datetime.datetime(1970, 1, 1)

    def getGenre(self, soup) -> str:
        return "booklive"

    def getCategory(self, soup) -> str:
        return "booklive"
    
    def getCoverArtUrl(self, soup) -> str:
        return "booklive"

    """
    Get stuff from booklive
    """
    def scrapeProduct(self, productUrl) -> Book:
        book = super().scrapeProduct(productUrl)
        return book
    
    
    

class BookCreator():
    SOURCES = {
        "www.python.org": ExampleRetriever,
        "booklive.jp": BookliveRetriever
    }
    
    def createBook(retriever) -> Book:
        pass

    """
    Create the appropriate Retriever. according to passed URL
    """
    def getProduct ( productUrl ) -> Book:
        parsed = urlparse( productUrl )
        host = parsed.hostname
        retriever = BookCreator.SOURCES[host]()
        return retriever.scrapeProduct(productUrl)
    

