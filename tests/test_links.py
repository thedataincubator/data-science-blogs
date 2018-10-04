import os
import re
import codecs
import pytest
import requests
from bs4 import BeautifulSoup
import markdown

def _get_files():
    return [i for i in os.listdir()
            if i.split('.')[-1] == 'md']

def _parse_links(filename):
    input_file = codecs.open(filename, 
                             mode="r", 
                             encoding="utf-8")
    text = input_file.read()
    soup = BeautifulSoup(markdown.markdown(text), "lxml")
    return [link['href'] for link in soup.find_all('a', href=True)]

def _valid(link):
    if '.md' in link:
        return False
    if '.csv' in link:
        return False
    if '.' not in link:
        return False
    return True

def _get_links_from_page(filename):
    links = []
    for link in _parse_links(filename):
        if _valid(link):
            links.append((filename, link))
    return links

def _get_links():
    links = []
    for filename in _get_files():
        links += _get_links_from_page(filename)
    return links

@pytest.mark.parametrize("filename,link", _get_links())
def test_link(filename, link):
    request_success = False
    for i in range(3):
        if request_success:
            break
        try:
            r = requests.get(link, timeout=10)
            request_success = True
        except Exception:
            pass

    assert request_success
    assert r.status_code == 200
