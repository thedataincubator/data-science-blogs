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

def _test_link(link):
    request_success = False
    for i in range(3):
        if request_success:
            break
        try:
            r = requests.get(link)
            request_success = True
        except Exception:
            print("error with", link)

    assert request_success
    assert r.status_code == 200

def _valid(link):
    if '.md' in link:
        return False
    if '.csv' in link:
        return False
    if '.' not in link:
        return False
    return True

@pytest.mark.parametrize("filename", _get_files())
def test_links(filename):
    for link in _parse_links(filename):
        if _valid(link):
            _test_link(link)
