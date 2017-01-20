import requests
import logging

logging.basicConfig(level=logging.INFO)

BEGIN_DT = '2016-01-19'
END_DT = '2017-01-19'


def get_cran_data(package_list, begin, end):
  """Get count of downloads from a CRAN mirror, in specified date range

  package_list: needs comma-separated string of package names
  begin, end like: '2016-01-19'
  """

  logging.warning("Using date range: {0} to {1}".format(begin, end))
  url = 'http://cranlogs.r-pkg.org/downloads/total/' + BEGIN_DT + ':' +\
        END_DT + '/' + formatted_packages
  r = requests.get(url)
  return r.json()


if __name__ == "__main__":
  import json
  from utils import read_package_txt

  package_list = read_package_txt("data/package-list-from-cran-task-view.txt")  # noqa
  formatted_packages = ','.join(package_list)
  data = get_cran_data(formatted_packages, begin=BEGIN_DT, end=END_DT)

  with open('data/cran_downloads.json', 'w') as f:
    json.dump(data, f)

