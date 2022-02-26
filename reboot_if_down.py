import os
import sys
import subprocess
import time

IFACE = os.environ['IFACE']
CARRIER_PATH = os.path.join(os.path.join('/sys/class/net', IFACE), 'carrier')
DELAY=float(os.environ.get('DELAY', '1.0'))
REBOOT_SCRIPT=os.environ.get('REBOOT_SCRIPT', '/opt/usb_reset/reboot_usb_device_by_id.py')

reboot = False

# Check if the file exists
if os.path.exists(CARRIER_PATH):
  # Check if the carrier is present
  with open(CARRIER_PATH) as fin:
    has_carrier = int(fin.read()) > 0

  if has_carrier:
    sys.stdout.write("interface %s has a carrier\n" % (IFACE,))
  else:
    sys.stdout.write("interface %s has no carrier\n" % (IFACE,))
  reboot = not has_carrier
else:
  sys.stdout.write("interface %s has no carrier file\n" % (IFACE,))
  reboot = True

sys.stdout.flush()
if not reboot:
  sys.exit(0)

subproc_env = dict(os.environ)
subproc_env['FLIP'] = '1'
cmd = ['python3', REBOOT_SCRIPT]
proc = subprocess.Popen(cmd, env = subproc_env)
exit_code = proc.wait()
if exit_code != 0:
  sys.stderr.write("failed running reboot script, exited %d\n" % (exit_code,))
  sys.exit(1)

for service in ['systemd-networkd', 'NetworkManager']:
  cmd = ['systemctl', 'restart', service]
  proc = subprocess.Popen(cmd)
  exit_code = proc.wait()
  if exit_code != 0:
    sys.stderr.write("restarting service %s failed, exited %d\n" % (service, exit_code,))
  time.sleep(DELAY)



