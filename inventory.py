import json
import platform
import psutil
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

   return base_dict


def main():
   file = open('inventory.json', 'w')

   base_dict = cross_platform_inventory.inventory()

   if (platform.system() == 'Windows'):
      json.dump(windows_inventory(base_dict), file)
   elif (platform.system() == 'Linux'):
      json.dump(linux_inventory(base_dict), file)
   else:
      json.dump('Unsupported OS', file)

   file.close()


main()