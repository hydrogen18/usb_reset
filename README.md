This is a proejct I created to reset a problematic USB WiFi stick. It sometimes fails, but unplugging it and plugging it back in fixes it. This does the closest equivalent, but in software.

This has 4 components

1. `reboot_usb_device_by_id.py` - a script to perform a software unplug and plug of a USB device. This works for any USB devices
2. `reboot_if_down.py` - a script that checks a network interface for connectivity and then runs the first script if it fails
3. `restart-network-if-down.service` - a systemd service that runs the second script
4. `restart-network-if-down-task.timer` - a systemd timer that triggers the service

# Installation

# Step 1

Clone this project to `/opt` on the target machine

# Step 2

Copy the following files to sytemd's location

```
::text

cp /opt/usb_reset/restart-network-if-down.service /etc/systemd/system
cp /opt/usb_reset/restart-network-if-down-task.timer /etc/systemd/system
```

# Step 3

Find the vendor ID and product ID of your USB WiFi device

```
::text

$ lsusb
Bus 005 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 004 Device 024: ID 0bda:2838 Realtek Semiconductor Corp. RTL2838 DVB-T
Bus 004 Device 023: ID 0bda:2838 Realtek Semiconductor Corp. RTL2838 DVB-T
Bus 004 Device 022: ID 0bda:2838 Realtek Semiconductor Corp. RTL2838 DVB-T
Bus 004 Device 021: ID 1a40:0101 Terminus Technology Inc. Hub
Bus 004 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 003 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
Bus 002 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 001 Device 002: ID 1737:0071 Linksys WUSB600N v1 Dual-Band Wireless-N Network Adapter [Ralink RT2870] < ----THIS ONE
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
```

The vendor ID is 1737 and the product ID is 0071 in my case.

Find the interface ID

```
::text

$ ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.112.90  netmask 255.255.255.255  broadcast 0.0.0.0
        inet6 fe80::6d1e:7923:256:bba  prefixlen 64  scopeid 0x20<link>
        ether 9a:e0:76:d2:9c:42  txqueuelen 1000  (Ethernet)
        RX packets 81221  bytes 10956089 (10.9 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 81758  bytes 10265014 (10.2 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
        device interrupt 43  

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 388727  bytes 43689190 (43.6 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 388727  bytes 43689190 (43.6 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

wlx001ee5d8d053: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.12.61  netmask 255.255.255.0  broadcast 192.168.12.255
        inet6 fe80::b7a0:6ef0:6a48:1f0a  prefixlen 64  scopeid 0x20<link>
        ether 00:1e:e5:d8:d0:53  txqueuelen 1000  (Ethernet)
        RX packets 545  bytes 55324 (55.3 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 311  bytes 44716 (44.7 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

```

In my case the WiFi interface starts with "wl" (all wireless interfaces should) and is "wlx001ee5d8d053".

Edit the file `/etc/systemd/system/restart-network-if-down.service` and then update the lines for `VENDOR_ID`, `PRODUCT_ID`, and `IFACE` to the values just found

# Step 4

Have systemd discover the new services by running `systemctl daemon-reload`

# Step 5 

Enable the timer by running `systemctl enable restart-network-if-down-task.timer`

# Step 6

That's it. The timer runs the service every 2 minutes and the network interface is not connected to a network it reboots the USB device, sysytemd-network, and NetworkManager.
