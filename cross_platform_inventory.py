import platform
import psutil
import socket

# TODO: obter modelo de processador
def get_cpu_info():
   return {
      'count': psutil.cpu_count(),
      'min_freq': psutil.cpu_freq().min,
      'max_freq': psutil.cpu_freq().max,
   }

# TODO: obter informações de discos (modelo, etc)
def get_disks_info():
   partitions = []

   for partition in psutil.disk_partitions():
      usage = psutil.disk_usage(partition.mountpoint)

      partitions.append({
         'device': partition.device,
         'mountpoint': partition.mountpoint,
         'type': partition.fstype,
         'total': usage.total,
         'used': usage.used,
         'free': usage.free,
      })
   
   return partitions

# TODO: obter infos de MHz
def get_memory_info():
   memory_info = psutil.virtual_memory()

   return {
      'total': memory_info.total,
      'total_swap': psutil.swap_memory().total,
   }


def get_sensors_info():
   sensors = {}

   temps = psutil.sensors_temperatures()

   if not temps:
      return sensors

   for name, entries in temps.items():
      sensors[name] = {}

      for entry in entries:
         sensors[name][entry.label or name] = {
            'current': entry.current,
            'high': entry.high,
            'critical': entry.critical,
         }
   
   return sensors

# TODO: get mac address, etc  
def inventory():
   hostname = socket.gethostname()

   return {
      'hostname': hostname,
      'ip': socket.gethostbyname(hostname),
      'arch': platform.architecture(),
      'machine': platform.machine(),
      'processor': platform.processor(),
      'system': platform.system(),
      'release': platform.release(),
      'version': platform.version(),
      'cpu': get_cpu_info(),
      'memory': get_memory_info(),
      'disks': get_disks_info(),
      'boot_time': psutil.boot_time(),
      'users': list(map(lambda user: user._asdict(), psutil.users())),
      'sensors': get_sensors_info()
   }