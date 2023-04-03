"""This is a module for multi-threading the scraping process with proxies and user-agents and such. """
import threading
import time
from mangaweb.Retriever.Retriever import ProductCreator

class ScraperThread(threading.Thread):
    """Scraper class that uses a proxy"""

    def __init__(self, urls, proxy) -> None:
        """Constructor for scraper thread class, that extends threading.Thread """
        threading.Thread.__init__(self)
        self.urls = urls
        self.proxy = proxy
        self.creator = ProductCreator()
        self.series_list = []

        # include the proxy if created with a proxy
        if proxy is not None:
            self.set_proxy( self.proxy )


    def set_proxy(self, proxy):
        """Set the proxy for the current thread and update the creator object's header"""
        proxies = {
            'http': f'http://{proxy}',
            'https': f'https://{proxy}',
        }
        self.creator.set_proxies( proxies )

    def set_header(self, headers):
        header = self.creator.headers
        if header is not None:
            header.update(headers)
        self.creator.set_headers(header)

    def __scrape(self) -> list:

        for url in self.urls:
            try:
                time.sleep(1)
                print (f'{str(self.proxy)} from {str(self.name)} on {url}' )
                series = self.creator.get_series(url)
                self.series_list.append(series.to_csv())
                

            except Exception as exception:
                print (f'FAILED: {str(self.proxy)} from {str(self.name)} on {url} {str(exception.args)}' )


    def run(self):
        self.__scrape()

    def join(self, *args):
        threading.Thread.join(self, *args)
