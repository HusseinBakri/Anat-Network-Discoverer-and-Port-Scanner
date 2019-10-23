#!/usr/bin/env python

import scapy.all as scapy
from mac_vendor_lookup import MacLookup
#for printing arguments help and available options for users
import optparse

'''
Description: This tool is part of the ethical hacking toolset. It describes a simple ARP network reconnaissance tool.
			 This is for educational use ONLY for security purposes.
The usage of Network Discoverer can be invoked via a -h switch
Requirements: You need only to install scapy, mac_vendor_lookup and optparse
          		Eg: 'pip3 install scapy'
          		Use packaged executables for Mac OS, Linux and MS Windows for deployment
Usage: python3 NetworkDiscoverer.py  or ./NetworkDiscoverer.py (after making the file executable or 
        better for deployment to change source code and package the app as executables
Enjoy!
'''

def ARPScan(IP):
	arp_request = scapy.ARP()
	arp_request.pdst =IP # setting the IPfield in Scapy ARP packet to IP	
	broadcast = scapy.Ether()
	broadcast.dst = "ff:ff:ff:ff:ff:ff"	
	arp_request_broadcast = broadcast/arp_request	
	answered_list, unanswered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)	
	clients_list = []
	for answer in answered_list:		
		RetrievedMACVendor = MacLookup().lookup(answer[1].hwsrc)
		client_dict = {"ip":answer[1].psrc, "mac":answer[1].hwsrc, "mac_vendor": RetrievedMACVendor}
		clients_list.append(client_dict)
	return clients_list


def PrintResults(Found_devices_list):
	if(not Found_devices_list):
		print("Sorry did not find any host/device after scanning....")
		exit(0)
	else:
		print("IP\t\tAt MAC Address\t\tMAC Vendor/Hostname\n")
		print("-----------------------------------------------------------")
		for device in Found_devices_list:
			print(device["ip"] + "\t\t" + device["mac"] + "\t\t" + device["mac_vendor"]  + "\n")


def main():
    parser = optparse.OptionParser('Usage of the program: ' + '-t <target IP>')
    parser.add_option('-t', '--target', dest='targetIP', type='string' , help='specify a target IP eg: 10.0.2.18 or 10.0.2.0/24 for the whole subnet)')

    (options, args) = parser.parse_args()
    targetIP = options.targetIP    

    if(options.targetIP == None):
    	parser.print_help()
    	exit(0)

    results = ARPScan(targetIP)
    PrintResults(results)


if __name__ == '__main__':
    main()


