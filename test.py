"""Requests to pull info from manga sites. Using get"""
import requests

"""Analyze the contents of HTML content from requests.content"""
from bs4 import BeautifulSoup

req = requests.get('https://google.com')
soup = BeautifulSoup(req.content, 'html.parser')
print(soup.prettify())
