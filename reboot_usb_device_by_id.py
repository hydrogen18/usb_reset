import os
import string
import time
import sys

USBFS_DEVICES = os.environ.get('USBFS_DEVICES','/sys/bus/usb/devices')
USBFS_DRIVERS = os.environ.get('USBFS_DRIVERS', '/sys/bus/usb/drivers')
#FIND_DRIVER = os.environ['FIND_DRIVER']
FLIP = int(os.environ.get('FLIP', '0')) > 0
VENDOR_ID=int(os.environ['VENDOR_ID'], 16)
PRODUCT_ID=int(os.environ['PRODUCT_ID'], 16)
VERBOSE=int(os.environ.get('VERBOSE', '1')) > 0
DELAY=float(os.environ.get('DELAY', '1.0'))

matching_device_ids = []

for entry in os.listdir(USBFS_DEVICES):
  # Skip anything not starting with a number
  if not entry[0] in string.digits:
    continue

  vendor_path = os.path.join(USBFS_DEVICES, entry, 'idVendor')
  product_path = os.path.join(USBFS_DEVICES, entry, 'idProduct')

  if not os.path.exists(vendor_path) or not os.path.exists(product_path):
    continue

  with open(vendor_path) as fin:
    entry_vendor_id = int(fin.read(), 16)
  with open(product_path) as fin:
    entry_product_id = int(fin.read(), 16)

  if entry_vendor_id != VENDOR_ID or entry_product_id != PRODUCT_ID:
    continue

  if VERBOSE:
    sys.stdout.write("USB %s [%04x:%04x]\n" % (entry, entry_vendor_id, entry_product_id,))
  matching_device_ids.append(entry)

if len(matching_device_ids) == 0:
  sys.stderr.write("no devices matched\n")
  sys.exit(1)

flip = set(matching_device_ids)

for f in flip:
  if VERBOSE:
    sys.stdout.write("unbinding USB device: %s\n" % (f,))
  if FLIP:
    with open('/sys/bus/usb/drivers/usb/unbind', 'wb') as fout:
      fout.write(bytes(f + "\n", 'ascii'))
if VERBOSE:
  sys.stdout.flush()
time.sleep(DELAY)

for f in flip:
  if VERBOSE:
    sys.stdout.write("binding USB device: %s\n" % (f,))
  if FLIP:
    with open('/sys/bus/usb/drivers/usb/bind', 'wb') as fout:
      fout.write(bytes(f + "\n", 'ascii'))

