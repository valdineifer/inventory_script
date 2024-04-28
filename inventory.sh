#!/bin/bash

inventory_url='http://localhost:4000/inventory'

if ! command -v python3 &>/dev/null; then
  echo "Python 3 is not installed. Exiting..."
  exit 1
fi

if ! command -v pip &>/dev/null; then
  echo "pip is not installed. Exiting..."
  exit 1
fi

python3 src/inventory.py