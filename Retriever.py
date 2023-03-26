"""Requests to pull info from manga sites. Using get"""
from __future__ import annotations
from abc import abstractmethod
import datetime
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import tldextract

class Series():
    """Encapsulate data of a Series"""
    # pylint: disable=too-many-instance-attributes, too-many-arguments

    def __init__(self, title,
                 authors = None,
                 started_publishing = datetime.datetime(1970, 1, 1),
                 ended_publishing = datetime.datetime(1970, 1, 1),
                 volumes = None,
                 genre = "",
                 category = "",
                 series_cover = ""
                 ) -> Series:
        """Series object constructor.

        Args:
            title (str): Title of the series
            authors (list, optional): List of authors. 
                Defaults to None.
            started_publishing (_type_, optional): Date that series started publishing. 
                Defaults to datetime.datetime(1970, 1, 1).
            ended_publishing (_type_, optional): Date that series ended publishing. 
                Defaults to datetime.datetime(1970, 1, 1).
            volumes (list, optional): List of Book objects that are in this series. 
                Defaults to None.
            genre (str, optional): Genre of series. Defaults to "".
            category (str, optional): Category of series. 
                Defaults to "".

        Returns:
            Series: Series object
        """
        self.title = title
        self.authors = authors
        self.started_publishing = started_publishing
        self.ended_publishing = ended_publishing
        self.volumes = volumes
        self.genre = genre
        self.category = category
        self.series_cover = series_cover

    @classmethod
    def series_lite(cls, title,
                 authors = None,
                 started_publishing = datetime.datetime(1970, 1, 1),
                 ended_publishing = datetime.datetime(1970, 1, 1),
                 genre = "",
                 category = "",
                 series_cover = "") -> Series:
        """Create a Series object without populating the volumes list with Books. 

        Args:
            title (str): Title of the series
            authors (list, optional): List of authors. Defaults to [].
            started_publishing (datetime, optional): Date series started publishing.
                Default datetime(1970, 1, 1).
            ended_publishing (datetime, optional): Date series when ended publishing.
                Default datetime(1970, 1, 1).
            genre (str, optional): Genre of series. Defaults to "".
            category (str, optional): Category of series. . Defaults to "".
            series_cover (str, optional): url to cover of series. Defaults to "".

        Returns:
            Series: Series object
        """
        return cls(title=title,
                   authors = authors,
                   started_publishing = started_publishing,
                   ended_publishing = ended_publishing,
                   genre = genre,
                   category = category,
                   volumes = [],
                   series_cover = series_cover
                   )

    def __str__(self) -> str:
        """Return a string representation of the Series

        Returns:
            str: string representation of calling Series object
        """
        series =  ("Series title: " + self.title +
                " \nAuthor(s): " + ', '.join( str(item) for item in self.authors ) +
                " \nStarted publishing: " + self.started_publishing.strftime("%m/%d/%Y") +
                " \nEnded publishing: " + self.ended_publishing.strftime("%m/%d/%Y") +
                " \nGenre: " + self.category +
                " \nCategory: " + self.category
                )
        # only print the number of volumes if the list is populated.
        if len(self.volumes) > 0:
            series = series + " \nNumber of volumes: " + str(len(self.volumes))

        return series

    def add_book_to_series( self, book ):
        """Add a book object to the volumes list.

        Args:
            book (Book): Book object to add to the series
        """
        if isinstance(book, Book):
            self.volumes.append(book)
            return
        raise TypeError("Attempt to insert a " + str(type(book)) + " to a series object")

class Book():
    """Encapsulates data about a Book"""

    # pylint: disable=too-many-instance-attributes, too-many-arguments

    def __init__(self, title,
                 volume = 0,
                 author = "None",
                 series = None,
                 publisher = "None",
                 published = datetime.datetime(1970, 1, 1),
                 cover_art_url = ""
                 ) -> Book:
        """Constructor for book

        Args:
            title (str): Constructor for book
            volume (int, optional): Volume number of book. Defaults to 0.
            author (str, optional): Author of book. Defaults to "None".
            series (str, optional): Name of series
            publisher (str, optional): Publisher of book. Defaults to "None".
            published (datetime, optional): Published date. Defaults to datetime(1970, 1, 1).
            cover_art_url (str, optional): URL to cover art. Defaults to "".

        Returns:
            Book: new instance of Book
        """
        if title is None :
            raise ValueError( "Attempt to construct book without a title" )
        self.title = title
        self.volume = volume
        self.author = author
        self.series = series
        self.publisher = publisher
        self.published = published
        self.cover_art_url = cover_art_url


    def __str__(self) -> str:
        """Return a string representation of this book.

        Returns:
            str: String representation of the calling book object.
        """
        return ("Book: " + self.title +
                " \nAuthor: " + self.author +
                " \nSeries: " + self.series +
                " \nPublisher: " + self.publisher +
                " \nPublished: " + self.published.strftime("%m/%d/%Y") +
                " \nCover Art URL: " + self.cover_art_url)

    def to_csv(self) -> str:
        """Return comma separated string representation of current object.

        Returns:
            str: comma separated string representation of current object
        """
        return ','.join(list(vars(self).keys()))


class Retriever():
    """Parent Retriever class. All inheriting classes must be inheriting:
        get_title()
        get_volume()
        get_author()
        get_series_name()
        get_publisher()
        get_published()
        get_genre()
        get_category()
        get_cover_art_url()

    """

    def __init__(self) -> Retriever:
        """Constructor for Retriever

        Returns:
            Retriever: Generic Retriever
        """
        self.url = ""

    @abstractmethod
    def get_title(self, soup) -> str:
        """Get the title from BeautifulSoup object.

        Args:
            soup (BeautifulSoup): HTML parsed BeautifulSoup

        Returns:
            str: title of product
        """


    @abstractmethod
    def get_volume(self, soup) -> str:
        """Get the volume number from BeautifulSoup object

        Args:
            soup (BeautifulSoup): HTML parsed BeautifulSoup

        Returns:
            str: volume number of product
        """


    @abstractmethod
    def get_author(self, soup) -> str:
        """Get the author name from BeautifulSoup object

        Args:
            soup (BeautifulSoup): HTML parsed BeautifulSoup

        Returns:
            str: author name of product
        """


    @abstractmethod
    def get_series_name(self, soup) -> str:
        """Get the series name from BeautifulSoup object

        Args:
            soup (BeautifulSoup): HTML parsed BeautifulSoup

        Returns:
            str: series name of product
        """


    @abstractmethod
    def get_publisher(self, soup) -> str:
        """Get the publisher name from BeautifulSoup object

        Args:
            soup (BeautifulSoup): HTML parsed BeautifulSoup

        Returns:
            str: publisher name of product
        """


    @abstractmethod
    def get_published(self, soup) -> datetime:
        """Get the published date from BeautifulSoup object

        Args:
            soup (BeautifulSoup): HTML parsed BeautifulSoup

        Returns:
            datetime: published date of product
        """


    @abstractmethod
    def get_genre(self, soup) -> str:
        """Get the genre from BeautifulSoup object

        Args:
            soup (BeautifulSoup): HTML parsed BeautifulSoup

        Returns:
            str: genre of product
        """


    @abstractmethod
    def get_category(self, soup) -> str:
        """Get the category from BeautifulSoup object

        Args:
            soup (BeautifulSoup): HTML parsed BeautifulSoup

        Returns:
            str: category of product
        """


    @abstractmethod
    def get_cover_art_url(self, soup) -> str:
        """Get the cover art url information from BeautifulSoup object.

        Args:
            soup (BeautifulSoup): HTML parsed BeautifulSoup

        Returns:
            str: url of cover art image
        """


    @abstractmethod
    def get_next_volume_url(self, soup) -> str:
        """Get the URL of the next volume (if it exists) from the BeautifulSoup object.

        Args:
            soup (BeautifulSoup): HTML parsed BeautifulSoup of a product

        Returns:
            str: url of the next volume if exists. If not existing, return None.
        """

    def __get_page_soup(self, product_url ) -> BeautifulSoup:
        """Perform requests.get and encapsulate resulting html in Soup

        Args:
            product_url (str): url of product

        Returns:
            BeautifulSoup: HTML parsed BeautifulSoup of url
        """
        req = requests.get( product_url, timeout=240)
        soup = BeautifulSoup(req.content, 'html.parser')
        return soup

    def scrape_product(self, product_url) -> Book:
        """Gather the product information and encapsualte in a Book object.

        Args:
            product_url (str): product url

        Returns:
            Book: Book object that encapsualtes the information found at the given site. 
            If no product found, returns None.
        """
        self.url = product_url
        soup = self.__get_page_soup( product_url )
        return Book(
            self.get_title(soup),
            self.get_volume(soup),
            self.get_author(soup),
            self.get_series_name(soup),
            self.get_publisher(soup),
            self.get_published(soup),
            self.get_cover_art_url(soup)
                    )

    def scrape_series(self, product_url) -> Series:
        """Gather the information about a series and encapsulate in a Series object. 
        Uses series_lite class method to avoid creating Book objects for every vol in series.

        Args:
            product_url (str): url of product

        Raises:
            Exception: Raised if url doesn't point to a valid product.

        Returns:
            Series: Series object encapsulating series info.
        """
        soup = self.__get_page_soup( product_url )
        book = self.scrape_product( product_url )

        if book is None :
            raise ValueError("No book found at specified url")

        series = Series.series_lite(
            title = book.title,
            authors = book.author.split(','),
            started_publishing = book.published,
            ended_publishing = book.published,
            genre = self.get_genre(soup),
            category = self.get_category(soup),
            series_cover = book.cover_art_url
            )

        return series


class ExampleRetriever(Retriever):
    """Here is an example retriever to base your Retrievers off of."""

    def get_title(self, soup) -> str:
        # select the text of the element that is class "call-to-action"
        # that is nested in ele with class "documentation-banner"
        # which is nested in ele w class "header-banner"
        title = soup.select_one('.header-banner .documentation-banner .call-to-action').text.strip()
        return title

    def get_volume(self, soup) -> str:
        volume = soup.select_one('.container .main-content .row .docs-by-version .widget-title')
        return volume.text.strip()

    def get_author(self, soup) -> str:
        return "python"

    def get_series_name(self, soup) -> str:
        return "python"

    def get_publisher(self, soup) -> str:
        return "python"

    def get_published(self, soup) -> datetime:
        return datetime.datetime(1970, 1, 1)

    def get_genre(self, soup) -> str:
        return "python"

    def get_category(self, soup) -> str:
        return "python"

    def get_cover_art_url(self, soup) -> str:
        return "https://www.python.org/static/img/python-logo.png"

    def get_next_volume_url(self, soup) -> str:
        return "https://docs.python.org/3/"


class BookliveRetriever(Retriever):
    """Retriever object for Booklive.jp"""

    def get_title(self, soup) -> str:
        title = soup.select_one(".product_info #product_display_1")
        if title:
            return title.text.strip()
        return None

    def get_volume(self, soup) -> str:
        # for booklive, volume number is consistently in url so extract from there
        matches = re.findall("(?<=vol_no/).*", self.url)
        if len(matches) > 0:
            return matches[0]
        return None

    def get_author(self, soup) -> str:
        author = soup.select_one(".product_info .meta .author.clearfix .multiple_links a")
        if author:
            return author.text.strip()
        return None

    def get_series_name(self, soup) -> str:
        series = soup.select_one(".detail_area.clearfix.ua_click .btn_subtitle h2")
        if series and len( re.findall("(.*?)\\xa0のシリーズ作品", series.text.strip()) ) > 0:
            return re.findall("(.*?)\\xa0のシリーズ作品", series.text.strip() )[0]
        return None

    def get_publisher(self, soup) -> str:
        # specs are the details of the product.
        specs = soup.select(".product_field.clearfix .product_specs .product_data.clearfix dd a")
        if len(specs) > 3:
            return specs[2].text.strip()
        return None

    def get_published(self, soup) -> datetime:
        return datetime.datetime(1970, 1, 1)

    def get_genre(self, soup) -> str:
        return "booklive"

    def get_category(self, soup) -> str:
        return "booklive"

    def get_cover_art_url(self, soup) -> str:
        return "booklive"

    def get_next_volume_url(self, soup) -> str:
        return None

class ProductCreator():
    """Class to create Product. Parent class of other Creator classes."""

    # Map of hostnames to the Retriever class to use when creating Books and Series.
    SOURCES = {
            "www.python.org": ExampleRetriever,
            "booklive.jp": BookliveRetriever
        }

    @staticmethod
    def get_host_name ( product_url ) -> str:
        """Get the hostname out of a product url.

        Args:
            product_url (str): url of product

        Returns:
            str: hostname of url
        """
        parsed = urlparse( product_url )
        return parsed.hostname

    @staticmethod
    def get_retriever_from_hostname( hostname ):
        """Get the appropriate retriever object from the SOURCES dictionary.

        Args:
            hostname (str): hostname to lookfor
        """
        if hostname in ProductCreator.SOURCES:
            return ProductCreator.SOURCES[hostname]()

        # remove any subdomains that may be in the hostname.
        extract = tldextract.extract( hostname )
        domain = extract.domain + '.' + extract.suffix
        if domain in ProductCreator.SOURCES:
            return ProductCreator.SOURCES[domain]()

        return None

class BookCreator(ProductCreator):
    """Class to create Book objects."""   

    @staticmethod
    def get_product ( product_url ) -> Book:
        """Static method to create the appropriate abstract Retriever, according to passed URL

        Args:
            product_url (str): url to a book

        Returns:
            Book: instance of Book class
        """
        host = BookCreator.get_host_name( product_url )
        retriever = BookCreator.get_retriever_from_hostname( host )
        return retriever.scrape_product(product_url)

class SeriesCreator(ProductCreator):
    """Class to create a series"""

    @staticmethod
    def get_series ( product_url ) -> Series:
        """Return a series object given a url to a book product. 

        Args:
            product_url (str): url to a book

        Returns:
            Series: instance of Series class
        """
        host = SeriesCreator.get_host_name( product_url )
        retriever = SeriesCreator.get_retriever_from_hostname( host )
        return retriever.scrape_series(product_url)
