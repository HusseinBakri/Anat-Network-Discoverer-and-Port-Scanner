#!/usr/bin/env python

import scapy.all as scapy
from mac_vendor_lookup import MacLookup
#for printing arguments help and available options for users
import optparse

# for coloring the terminal
from termcolor import cprint, colored

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
def display_header():
        cprint(
            """\
  


                          _     _   _        _                          _      _____   _                                              
     /\                  | |   | \ | |      | |                        | |    |  __ \ (_)                                             
    /  \    _ __    __ _ | |_  |  \| |  ___ | |_ __      __ ___   _ __ | | __ | |  | | _  ___   ___  ___ __   __ ___  _ __  ___  _ __ 
   / /\ \  | '_ \  / _` || __| | . ` | / _ \| __|\ \ /\ / // _ \ | '__|| |/ / | |  | || |/ __| / __|/ _ \\ \ / // _ \| '__|/ _ \| '__|
  / ____ \ | | | || (_| || |_  | |\  ||  __/| |_  \ V  V /| (_) || |   |   <  | |__| || |\__ \| (__| (_) |\ V /|  __/| |  |  __/| |   
 /_/    \_\|_| |_| \__,_| \__| |_| \_| \___| \__|  \_/\_/  \___/ |_|   |_|\_\ |_____/ |_||___/ \___|\___/  \_/  \___||_|   \___||_|   
                                                                                                                                      
                                                                                                                                      

                                                  
                                              
             by Dr. Hussein Bakri\n""", 'green')
        cprint("This tool is licensed under MIT\n",'green')


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
		dash = '-' * 106
		cprint(dash)
		cprint('{:<40s}{:<40s}{:<40s}'.format('IP','At MAC Address', 'MAC Vendor/Hostname'))
		cprint(dash)   
		
		for device in Found_devices_list:
			cprint('{:<40s}{:<40s}{:<40s}'.format(device["ip"], device["mac"],  device["mac_vendor"]))



def main():
    parser = optparse.OptionParser('Usage of the program: ' + '-t <target IP>')
    parser.add_option('-t', '--target', dest='targetIP', type='string' , help='specify a target IP eg: 10.0.2.18 or 10.0.2.0/24 for the whole subnet)')

    (options, args) = parser.parse_args()
    display_header()

    targetIP = options.targetIP    

    if(options.targetIP == None):
    	parser.print_help()
    	exit(0)

    results = ARPScan(targetIP)
    PrintResults(results)


if __name__ == '__main__':
    main()


