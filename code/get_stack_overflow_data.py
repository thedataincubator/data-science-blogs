import requests
import urllib2
import logging

logging.basicConfig(level=logging.INFO)


GLOBAL_PARAMS = {
    "site" : "stackoverflow",
    "key" : "y38PeNERQJQIC8EPliKAVQ(("
}

# SO api is NOT case-sensitive
# package_list = ['dplyr', 'digest', 'ggplot2', 'rcpp', 'the']


def get_tag_counts(tag_list):
    """"Given tag list, return tag counts as json"""
    
    formatted_tags = ';'.join(tag_list)
    url = "https://api.stackexchange.com/2.2/tags/" + formatted_tags + "/info"
  
    try:
        r = requests.get(url, params=GLOBAL_PARAMS)
        if r.json()['has_more']:
            print "WARNING: Request has more data than is not shown here."
        return r.json()['items']
    except:
        logging.warning("Error in response.")


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


if __name__=="__main__":
  import json
  from utils import read_package_txt

  package_list = read_package_txt("../package-list-from-cran-task-view.txt")
  logging.info("Getting tags...")
  tag_counts = get_tag_counts(package_list)
  logging.info("Getting body counts (<60 seconds)...")
  question_body_counts = { item: get_body_count(item) for item in package_list}
  logging.info("Getting body counts with R tag (<60 seconds)...")
  question_body_counts_r = { item: get_body_count(item, tag='r')
                             for item in package_list}

  logging.info("Writing to disk...")
  with open('../data/so_tags.json', 'w') as f:
    json.dump(tag_counts, f)
  with open('../data/body_counts.json', 'w') as f:
    json.dump(question_body_counts, f)
  with open('../data/body_counts_r.json', 'w') as f:
    json.dump(question_body_counts_r, f)
  logging.info("DONE.")  

