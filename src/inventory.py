import http.client, urllib.parse
import json
import platform
import psutil
import sys

import cross_platform_inventory

def windows_inventory(base_dict):
   base_dict['windows'] = {
      'version': platform.win32_ver(),
      'edition': platform.win32_edition(),
      'services': list(psutil.win_service_iter()),
   }
   
   return base_dict


def linux_inventory(base_dict):
   base_dict['linux'] = {}

   for item in platform.freedesktop_os_release().items():
      base_dict['linux'][item[0].lower()] = item[1]

   base_dict['system_full'] = ' '.join([
      'Linux',
      base_dict['linux']['name'],
      base_dict['linux']['version'],
   ])

   return base_dict


def send_inventory(file_content):
   # parsed_body = urllib.parse.urlencode(file_content)

   parsed_url = urllib.parse.urlparse(sys.argv[1])

   conn = http.client.HTTPConnection(parsed_url.hostname, parsed_url.port)
   conn.request("POST", parsed_url.path, file_content, { "Content-type": "application/json" })
   response = conn.getresponse()
   
   print(response.status, response.reason)
   print(json.dumps(json.loads(response.read().decode('utf-8')), indent=2))
   
   conn.close()


def main():
   file = open('inventory.json', 'w+')

   base_dict = cross_platform_inventory.inventory()

   if (platform.system() == 'Windows'):
      json.dump(windows_inventory(base_dict), file)
   elif (platform.system() == 'Linux'):
      json.dump(linux_inventory(base_dict), file)
   else:
      json.dump('Unsupported OS', file)

   file.seek(0)
   file_content = file.read()
   file.close()
   
   send_inventory(file_content)


main()