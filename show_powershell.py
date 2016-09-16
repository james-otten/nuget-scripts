#James Otten 2016

import zipfile
import sys
import os
from termcolor import colored

if len(sys.argv) != 2:
  print('Usage:')
  print(' python %s <nuget_package>')
  print(' python %s <nuget_package_dir>')
  print('   where nuget_package is a nuget package')
  print('         nuget_package_dir is a directory containing nuget packages')
  exit(1)
  
path = sys.argv[1]

def show_powershell(file_path):
  zf = zipfile.ZipFile(file_path, 'r')
  for zipped_file_name in zf.namelist():
    if '.ps1' in zipped_file_name:
      print(colored('START %s/%s' % ( file_path, zipped_file_name), 'green'))
      data = zf.read(zipped_file_name)
      print(data)

if os.path.isdir(path):
  for filename in os.listdir(path):
    file_path = '%s/%s' % (path, filename)
    show_powershell(file_path)
else:
  file_path = sys.argv[1]
  show_powershell(file_path)
      
