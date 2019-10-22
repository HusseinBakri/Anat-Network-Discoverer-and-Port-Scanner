#!/usr/bin/python

from socket import *
# for coloring stuff in the terminal
from termcolor import colored
#for printing arguments help and available options for users
import optparse
# for threading
from threading import *
import re

'''
Description: This tool is part of the ethical hacking toolset. This is for educational use ONLY for security purposes.
The usage of Port Scanner can be invoked via a -h switch
Requirements: You need only to install termcolor
          		'pip3 install termcolor'
          		Use packaged executables for Mac OS, Linux and MS Windows for deployment
Usage: python3 PortScanner.py  or ./PortScanner.py (after making the file executable or 
        better for deployment to chnage source code and package the app as executables
Enjoy!
'''

def connScan(targetHost, targetPort):
        banner = ""
        try:
                socketconnection = socket(AF_INET, SOCK_STREAM)	#AF_INET fo IPv4, SOCK_STREAM for TCP
                #socketconnection = socket()
                socketconnection.connect((targetHost, targetPort))
    	
                try:
                        # The banner usually contains service name, version or OS (stripped from newlines)
                        banner = socketconnection.recv(1024).strip()
                        print(banner)
                        print(colored(str(targetPort) + '/tcp Open   {bannerStr}'.format(bannerStr=banner if banner is not None else "") , "green"))
                except:
                        banner = ""
                        print(colored(str(targetPort) + '/tcp Open   {bannerStr}'.format(bannerStr=banner if banner is not None else "") , "green"))
                        pass

    	
        except:
                print(colored(str(targetPort) + '/tcp Closed  {bannerStr} '.format(bannerStr=banner if banner is not None else "")  ,"red"))
        finally:
                socketconnection.close()

    

def portScan(targetHost, targetPorts):
	try:
		targetIP = gethostbyname(targetHost)
		
	except:
		print('Unknown host %s' %targetHost)

	try:
		targetAddressInfo = gethostbyaddr(targetIP)	#gives a tuple (hostname, list, IP)

		print('Scan Results for' + targetAddressInfo[0])


	except:
		print('Scan Results for' + targetIP)


	setdefaulttimeout(2)	#timeout in seconds
	for targetPort in targetPorts:
		t = Thread(target=connScan, args=(targetHost, int(targetPort)))
		t.start()


def main():
    parser = optparse.OptionParser('Usage of the program: ' + '-H <target host> -p <target port(s)>')
    parser.add_option('-H', '--host', dest='targetHost', type='string' , help='specify a target host (IP or discoverable domain name)')
    parser.add_option('-p', '--ports', dest='targetPort', type='string' , help='specify a single port or target ports sperated by commas eg: 22, 80, 443')

    (options, args) = parser.parse_args()
    targetHost = options.targetHost
    targetPorts = str(options.targetPort).split(',')

    if(options.targetPort == None):
    	parser.print_help()
    	exit(0)

    
    if(targetHost == None) | (targetPorts == None):
        #print(parser.usage)
        parser.print_help()
        exit(0)
    
    portScan(targetHost, targetPorts)    


if __name__ == '__main__':
    main()


    



