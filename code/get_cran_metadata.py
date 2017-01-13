import requests
import logging
import utils as ut

logging.basicConfig(level=logging.INFO)

BEGIN_DT = '2016-01-10'
END_DT = '2017-01-10'

def get_cran_data(begin=BEGIN_DT, end=END_DT):
  """Get count of downloads from rstudio cran, in specified date range"""
  
  logging.warning("Using date range: {0} to {1}".format(begin, end))
  package_list = ut.read_package_txt("../package-list-from-cran-task-view.txt")
  formatted_packages = ','.join(package_list)
  url = 'http://cranlogs.r-pkg.org/downloads/total/' + BEGIN_DT + ':' +\
        END_DT + '/' + formatted_packages
  r = requests.get(url)
  return r.json()


if __name__ == "__main__":
  import json
  logging.info("Getting CRAN data...")
  data = get_cran_data()
  with open('../data/cran_metadata.json', 'w') as f:
    json.dump(data, f)
  logging.info("DONE.")
