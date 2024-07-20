import json
import platform
import psutil
import sys
import requests
from uuid import uuid4
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


def get_token():
   file = open('/root/inventory_token', 'w+')
   token = file.read()

   if (token):
      file.close()
      return token
   
   token = str(uuid4())

   file.write(token)
   file.close()

   return token


def send_inventory(file_content):
   response = requests.post(
      sys.argv[1],
      allow_redirects=True,
      data=file_content,
      headers={
         "Content-type": "application/json",
         "Authorization": f"Bearer {get_token()}",
      }
   )

   print(response.status_code, response.reason)

   try:
      print(response.json())
   except requests.JSONDecodeError:
      print(response.text)


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