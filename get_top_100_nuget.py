#James Otten 2016

import requests
from pyquery import PyQuery as pq
import os
from time import gmtime, strftime

package_dir = 'packages' + strftime("%Y-%m-%d_%H:%M:%S", gmtime())
os.mkdir(package_dir)

packages = []

d = pq(url='https://www.nuget.org/stats/packages')
for a in d('.statistics-rank + td > a'):
  packages.append(str(a.text))

for package in packages:
  package_page = 'https://www.nuget.org/packages/%s' % package
  print(package_page)
  d = pq(url=package_page)
  download_url = d('a[title="Download the raw nupkg file."]').attr('href')
  print(download_url)
  file_name = '%s/%s.nupkg' % (package_dir, '.'.join(download_url.split('/')[-2:]))
  print(file_name)
  with open(file_name, 'wb') as handle:
    res = requests.get(download_url, stream=True)
    for block in res.iter_content(1024):
        handle.write(block)

