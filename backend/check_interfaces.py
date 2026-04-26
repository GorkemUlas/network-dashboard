from scapy.all import get_if_list
from scapy.arch.windows import get_windows_if_list

for iface in get_windows_if_list():
    print(iface['name'], '|', iface['description'])