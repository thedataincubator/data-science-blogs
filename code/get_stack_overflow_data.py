import requests
import urllib2
import logging

logging.basicConfig(level=logging.WARN)


GLOBAL_PARAMS = {
    "site" : "stackoverflow",
    "key" : "y38PeNERQJQIC8EPliKAVQ(("
}

# SO api is NOT case-sensitive
# package_list = ['dplyr', 'digest', 'ggplot2', 'rcpp', 'the']


def get_tag_counts(tag_list):
  """"Given tag list, return counts as json"""
   
  formatted_tags = ';'.join(tag_list)
  tag_url = "https://api.stackexchange.com/2.2/tags/"
  url = tag_url + formatted_tags + "/info?site=stackoverflow"

  r = requests.get(url)
  if r.json()['has_more']:
    logging.warning("Request has more data than is not shown here.")
  return r.json()['items']


def get_body_count(body_string, tag=None):
  """Given ONE string, return number of SO questions containing it

  possibly tagged with TAG
  uses filter=total to return counts only
  """
  baseurl = 'https://api.stackexchange.com/2.2/search/advanced'
  params = {
    'q': body_string,
    'filter': 'total',
  }
  params.update(GLOBAL_PARAMS)
  if tag:
    params.update({'tagged': tag})
  r = requests.get(baseurl, params=params)
  return r.json()['total']


# tag_counts = get_tag_counts(package_list)
# question_body_counts = { item: get_body_count(item) for item in package_list}

# print tag_counts
# print question_body_counts
  
