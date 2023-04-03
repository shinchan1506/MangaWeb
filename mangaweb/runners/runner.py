"""Requests to pull info from manga sites. Using get"""
import csv
from mangaweb.runners.HttpProxyList import HttpProxyList
from mangaweb.Retriever.Retriever import ProductCreator
from mangaweb.Scraper.ScraperThread import ScraperThread
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #temporary




proxies = HttpProxyList.get_valid_proxies()
thread_req_limit = 10
threads = []
used_proxy = 0


for id in range(1000, 1020, thread_req_limit):
    """primitive way of getting the links of the booklive catalogue.
    TODO: create a way to get the links out of https://booklive.jp/search/keyword/g_ids/1,2,3,4,5,6,7/page_no/1"""

    urls = [f'https://booklive.jp/product/index/title_id/{id}/' for id in range(id, id + thread_req_limit) ]
    thread = ScraperThread(urls = urls, proxy=proxies[used_proxy])
    threads.append(thread)
    used_proxy += 1

# start all scraping threads
for thread in threads:
    thread.start()

# wait for all threads to terminate
for thread in threads:
    thread.join()

# get value of all threads
with open("test.csv", "w+") as csv_file:
    writer = csv.writer(csv_file, delimiter=',', quotechar='\'', quoting=csv.QUOTE_NONE)
    creator = ProductCreator()
    writer.writerow(creator.get_series('https://booklive.jp/product/index/title_id/1000/').get_csv_header())

    for thread in threads:
        writer.writerows(thread.series_list)
