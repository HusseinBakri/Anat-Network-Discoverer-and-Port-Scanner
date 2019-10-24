#!/usr/bin/env python
from mac_vendor_lookup import MacLookup
#for printing arguments help and available options for users
import optparse

'''
Description: This script gets you the Mac Vendor when you give it a MAC Address.
			 It is needed to deduce things such as Routers, mobile devices etc...
The usage of GetMeMACVendor can be invoked via a -h switch
Requirements: You need only to install  mac_vendor_lookup and optparse
          		Eg: 'pip3 install mac_vendor_lookup'
          		Use packaged executables for Mac OS, Linux and MS Windows for deployment
Usage: python3 GetMeMACVendor.py  or ./GetMeMACVendor.py (after making the file executable or 
        better for deployment to change source code and package the app as executables
Enjoy!
'''

def main():
    parser = optparse.OptionParser('Usage of the program: ' + '-m <MAC Address>')
    parser.add_option('-M', '--MAC', dest='MACAddress', type='string' , help='specify a MAC Address to get MAC vendor)')

    (options, args) = parser.parse_args()
    MACAddress = options.MACAddress    

    if(options.MACAddress == None):
    	parser.print_help()
    	exit(0)

    if(MACAddress.lower() == "ff-ff-ff-ff-ff-ff"):
        print("Broadcast MAC address of FF:FF:FF:FF:FF:FF")
    else:    
        RetrievedMACVendor = MacLookup().lookup(MACAddress)
        print("Mac Vendor of your specified MAC Address is: " + RetrievedMACVendor)


if __name__ == '__main__':
    main()