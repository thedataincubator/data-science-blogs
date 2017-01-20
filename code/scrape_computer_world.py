import requests
import pandas as pd
from bs4 import BeautifulSoup

URL = 'http://www.computerworld.com/article/2921176/business-intelligence/great-r-packages-for-data-import-wrangling-visualization.html'  # noqa

r = requests.get(URL)
soup = BeautifulSoup(r.text, 'lxml')
table = soup.find('table', id='cwsearchabletable')
pd_table = pd.read_html(str(table))
if len(pd_table) != 1:
    print 'WARNING: multiple tables found.  I am using the first one only.'
df = pd.DataFrame(pd_table[0])

# HERE IS A LIST OF THE R PACKAGES from that link
print list(df.Package)
