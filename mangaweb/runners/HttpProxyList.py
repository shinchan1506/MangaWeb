"""This module is used for generating a list of active http proxies"""
import re
import threading
from bs4 import BeautifulSoup
import requests


class testThread (threading.Thread):
    """Thread for testing tghe proxy with google"""
    
    def __init__(self, proxy):
        """Constructor for testing the proxy on google"""
        threading.Thread.__init__(self)
        self.valid_proxy = False
        self.proxy = proxy
    
    def test_proxy(self):
        """Test if 200 response returned from google using proxy"""
        proxies = {
            'http': f'http://{self.proxy}',
            'https': f'https://{self.proxy}',
        }
        try:
            rsp = requests.get('https://www.google.com', proxies=proxies, verify=False, timeout=5)
            return rsp.status_code == 200
        except Exception as exception:
            pass
        
        return False
        
    
    def run(self):
        """run the thread"""
        self.valid_proxy = self.test_proxy()


class HttpProxyList():
    """Class to retrieve a list of free proxies"""

    @classmethod
    def __get_proxies(cls):
        """Get a list of proxies as str (includes ports) from free source.

        Returns:
            list: list of proxies as str (includes ports)
        """
        regex = r"[0-9]+(?:\.[0-9]+){3}:[0-9]+"
        c = requests.get("https://free-proxy-list.net/")
        soup = BeautifulSoup(c.content, 'html.parser')
        z = soup.find('textarea').get_text()
        x = re.findall(regex, z)
        return [str(proxy) for proxy in x]
    
    @classmethod
    def __create_test_proxy_threads(cls, proxy_list):
        """Create and return testThread objects for each proxy in proxy_list

        Args:
            proxy_list (list): list of proxies as strings (include ports)

        Returns:
            list: list of testThread objects 
        """
        threads = []
        for proxy in proxy_list:
            threads.append(testThread(proxy))
        return threads

    @classmethod
    def __start_test_proxy_threads(cls, proxy_thread_list):
        """Start the proxy threads that are passed

        Args:
            proxy_thread_list (list): list of testThread
        """
        for proxy_thread in proxy_thread_list:
            proxy_thread.start()

        # wait for the threads to terminate
        for proxy_thread in proxy_thread_list:
            proxy_thread.join()

    @classmethod
    def __get_test_results(cls, proxy_thread_list):
        """Check each proxy thread for whether response status code was 200 or not.
        Only returns the ones that got a 200."""
        valid_proxies = []
        for proxy_thread in proxy_thread_list:
            if proxy_thread.valid_proxy:
                valid_proxies.append(proxy_thread.proxy)
        return valid_proxies

    @classmethod 
    def get_valid_proxies(cls):
        """Return a list of valid proxies that are tested in multiple threads"""
        proxies = cls.__get_proxies()
        threads = cls.__create_test_proxy_threads(proxies)
        cls.__start_test_proxy_threads(threads)
        return cls.__get_test_results(threads)
