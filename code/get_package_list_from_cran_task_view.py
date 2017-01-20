import requests
import re
from bs4 import BeautifulSoup

URL = 'https://cran.r-project.org/web/views/MachineLearning.html'


def get_package_list(url):
  """ scrape URL for list of ML packages, which appears near bottom

  + use regex to remove "(text)" from package name"""
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'lxml')
  h3 = soup.find('h3')
  descendants_list = h3.findNextSibling().text.strip().split("\n")
  return [re.sub(" \([A-z]+\)", "", item) for item in descendants_list]


if __name__ == "__main__":
  package_list = get_package_list(URL)
  print "Found {0} packages.".format(len(package_list))
  with open("../package-list-from-cran-task-view.txt", "w") as f:
    f.write(','.join(package_list))
