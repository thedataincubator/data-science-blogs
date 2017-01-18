import sys
import logging
import requests


def search_repo_return_star_info(repo_query, lang='r', add_str=None,
                                 token=None):
  """Search github for repo, take top result, and
  return {repo_name: stars} or None

  lang = search in language. can use None
  add_str = additional string to pass
  token = github api token. should not be None
  """
  if token is None:
    sys.exit("Need github api token passed as string")

  logging.debug(repo_query)
  headers = {'Authorization': 'token %s' % token}
  q = repo_query
  if add_str is not None:
    q = q + '%20' + add_str
  if lang is not None:
    q = q + "+language:" + lang

  try:
    logging.debug("Request processing...")
    repo_info = requests.get(
      'https://api.github.com/search/repositories?q=' + q, headers=headers)
    if repo_info.json()['total_count'] is not 0:
      logging.info("Found {0} repos for query '{1}' in language '{2}' and add_str '{3}.".format(  # noqa
        repo_info.json()['total_count'], repo_query, lang, add_str))
      return {repo_info.json()['items'][0]['full_name']:
              repo_info.json()['items'][0]['stargazers_count'],
              "package_name": repo_query}
    else:
      logging.warning("No data found or other response error for query '{0}'".format(repo_query))  # noqa
      pass
  except:
    logging.warning("Request failed for query '{0}'".format(repo_query))
    print repo_info.json()
    pass


if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)
  with open("./secrets/github-token.nogit", "rb") as f:
    token = f.read()

  if len(sys.argv) == 1:
    repo_query = "dplyr"
  else:
    repo_query = str(sys.argv[1])

  res = search_repo_return_star_info(repo_query, token=token)
  print res
