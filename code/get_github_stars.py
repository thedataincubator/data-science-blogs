import logging
import requests

logging.basicConfig(level=logging.INFO)


def to_api(x):
  """Return correct github repo link for API call"""
  return x.replace('/issues', "").replace('github.com', 'api.github.com/repos')


def get_stars(url):
  """Given github api url, request content and return stargazers_count"""
  r = requests.get(url)
  return r.json()['stargazers_count']


if __name__ == '__main__':
  import json

  with open("data/package_urls.json", "r") as f:
    urls = json.load(f)

  github_api_links = {k: to_api(v['github_url']) for k, v in urls.iteritems()
                      if v['github_url'] is not None}
  stars = {pkg: get_stars(url) for pkg, url in github_api_links.iteritems()}

  with open("data/github_stars.json", "w") as f:
    json.dump(stars, f)
