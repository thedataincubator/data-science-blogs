import requests
from bs4 import BeautifulSoup
import logging


def get_urls_for_pkg(package):
    """Given package, find its webpage and extract package source links
    (incl. github)

    source links: URL and BUGURL (as available)
    see example: https://cran.r-project.org/package=ranger
    Grab the URL and the BugReports URL. Ultimately, we want the github repo
    link."""

    BASEURL = "https://cran.r-project.org/"

    urls = None
    bug_urls = None
    all_urls = None
    github_url = None

    r = requests.get(BASEURL + "package=" + package)
    soup = BeautifulSoup(r.text, 'lxml')
    body = soup.select('body')[0]

    url_ = body.findNext('td', text='URL:')
    bug_ = body.findNext('td', text='BugReports:')

    if url_ is not None:
        urls = [url.text for url in url_.findNext('td').findAll('a')]
    if bug_ is not None:
        bug_urls = [url.text for url in bug_.findNext('td').findAll('a')]
    # some or both of (urls, bug_urls) may be None:
    if urls is not None:
        all_urls = list(set(urls + bug_urls if bug_urls is not None else urls))
    if all_urls is not None:
        github_url = [url for url in all_urls if 'github' in url.lower()]
    # return any one github url, or None:
    # (there may be main github link + 'issues' link)
    github_url = next(iter(github_url or []), None)

    logging.info("Found urls: {0}".format(all_urls))
    return {"github_url": github_url, "all_urls": all_urls}


if __name__ == '__main__':
  import json
  import utils as utils

  logging.basicConfig(level=logging.INFO)

  package_list = utils.read_package_txt("data/package-list-from-cran-task-view.txt")  # noqa
  urls = {}
  urls = {package: get_urls_for_pkg(package) for package in package_list}

  with open("data/package_urls.json", "w") as f:
    json.dump(urls, f)
