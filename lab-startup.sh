#!/bin/bash

if ! command -v python3 &>/dev/null; then
  echo "Python 3 is not installed. Exiting..."
  return 1
fi

if ! command -v pip &>/dev/null; then
  echo "pip is not installed. Exiting..."
  return 1
fi

inventory_path="/etc/gdm3/PostLogin/inventory_script-master"

if [ -d "$inventory_path" ]; then
  echo "Inventory script already installed. Exiting..."
  return 0
fi

wget -O inventory.zip https://github.com/valdineifer/inventory_script/archive/refs/heads/master.zip
unzip -o inventory.zip -d /etc/gdm3/PostLogin

if [ -f /etc/gdm3/PostLogin/Default ]; then
  mv /etc/gdm3/PostLogin/Default /etc/gdm3/PostLogin/Default.bkp
fi

inventory_url='https://inventory-server-ivory.vercel.app/inventory'

pip install -r "$inventory_path/src/requirements.txt"

echo "#!/bin/bash
python3 $inventory_path/src/inventory.py $inventory_url &> /var/log/inventory.log
exit 0
" > /etc/gdm3/PostLogin/Default

chmod a+x /etc/gdm3/PostLogin/Default

exit 0