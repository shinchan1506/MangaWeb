"""Requests to pull info from manga sites. Using get"""
from bs4 import BeautifulSoup
import requests

req = requests.get('https://google.com', timeout=240)
soup = BeautifulSoup(req.content, 'html.parser')
print(soup.prettify())
