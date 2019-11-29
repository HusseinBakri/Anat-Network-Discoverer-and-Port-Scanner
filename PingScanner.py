#!usr/bin/python3

# for coloring the terminal
from termcolor import cprint, colored

# for printing arguments help and available options for users
import argparse

import subprocess
# from subprocess import Popen, PIPE

import sys

# For detecting the OS the script is working on
import platform

import socket

import struct


'''
Description: This tool is a ping scanner (i.e. using icmp). You can give it a range and a base IP and it
ping all the IPs that follow these criteria to check if they are reachable

Requirements:
------------
Install all modules needed by this program. Per example to install termcolor by pip: pip install termcolor

You can also package it as an executable. Per example an .exe for Windows. Please follow the documentation 
of the repository on how to do that for your particular OS.

Usage: 
-----
python PingScanner.py  --base 172.217.169 --range 46-48

When you provide less than 3 parts as a base it fill the missing part with 0 same as the behaviour of
socket class in Python

python PingScanner.py  --base 172.217 --range 46-48

python PingScanner.py  --base 172.217 --range 46-48

Dr. Hussein Bakri
Enjoy!
'''
def display_header():
        cprint(
            """\
  


                          _     _____  _                  _____                                       
     /\                  | |   |  __ \(_)                / ____|                                      
    /  \    _ __    __ _ | |_  | |__) |_  _ __    __ _  | (___    ___  __ _  _ __   _ __    ___  _ __ 
   / /\ \  | '_ \  / _` || __| |  ___/| || '_ \  / _` |  \___ \  / __|/ _` || '_ \ | '_ \  / _ \| '__|
  / ____ \ | | | || (_| || |_  | |    | || | | || (_| |  ____) || (__| (_| || | | || | | ||  __/| |   
 /_/    \_\|_| |_| \__,_| \__| |_|    |_||_| |_| \__, | |_____/  \___|\__,_||_| |_||_| |_| \___||_|   
                                                  __/ |                                               
                                                 |___/                                                

                                                  
                                              
             by Dr. Hussein Bakri\n""", 'green')
        cprint("This tool is licensed under MIT\n",'green')

def main():
	parser = argparse.ArgumentParser(description="A ping (ICMP) scanner of a range of IPs")
	parser.add_argument('--base', type=str, help="Enter a base IP  exactly such as 192.168.56 no dot at the end\nIf you provide an base IP with less than three dots, the missing parts are padded with 0s")
	parser.add_argument('--range', type=str, help="Enter a range of IPs seperated by - exactly like 0-255 or 100-200\n100-200 means you want to ping all IP with BASE.100 to BASE.200")

	args = parser.parse_args()
	display_header()


	if (args.base == None):
		parser.print_help()
		exit(0)
	# if (args.range == None):
	# 	parser.print_help()
	# 	exit(0)

	if(len(vars(args)) == 0):
		parser.print_help()
		exit(0)
	

	if args.base and args.range:
		ping(args.base, args.range)
	elif args.base and (args.range==None):
		ping(args.base, '0-0')
	else:
		parser.print_help()
		exit(0)



def ping(base, given_range):
	IPrange = given_range.split('-')
	try:
		RangeLower = int(IPrange[0])
		RangeHigher = int(IPrange[1])+1
	except ValueError:
		exit("One of the boundaries of your range is not a number or your range is not formatted correctly. \nCorrect format: 2-200")
	
	if(RangeHigher > 255):
		exit("Upper Range is higher than 255")
	
	if(RangeLower < 0):
		exit("Lower Range is lower than 0")

	if(RangeHigher < RangeLower):
		exit("Higher Range is lower than Lower Range")
	
	# Checking for the case when user put a complete IP instead of a base IP
	# len(base.strip().split(".")) would be = 4 if a complete IP
	# Initially BaseIsCompleteIP is considered not the case
	BaseIsCompleteIP = False
	if len(base.strip().split(".")) == 4:
		BaseIsCompleteIP = True
		cprint("Your base IP is a complete IP. I am checking it only and ignoring any range.\n")


	try:
		
		BinaryIP= socket.inet_aton(base)
		baseIP = base + '.'
		DottedIP= socket.inet_ntoa(BinaryIP)
 
		# cprint("\nConsidering your baseIP as: {0}".format(DottedIP),"green")
	except socket.error:
		exit("Your base IP does not look like an IP or part of an IP. It should be like per example: 192.168.56 ")

	#Check OS since -n is for MS Windows and -c for Linux and MacOS
	if (platform.system()=='Windows'):
		switch = "-n"
	elif(platform.system()=='Linux' or platform.system()=='Darwin'):
		switch = "-c"
	else:
		switch = "-c"
	
	if BaseIsCompleteIP:
		RangeLower=0
		RangeHigher=1

	for i in range(RangeLower, RangeHigher):
		IP = baseIP + str(i)

		if BaseIsCompleteIP:
			IP=base
		

		# Ping Exit status and their meaning
		# Success: code 0
		# No reply: code 1
		# Other errors: code 2 check_output
		IPNumberOfDots = IP.split(".")

		ProcessOutput = subprocess.Popen(["ping", switch, "1", IP], stdout = subprocess.PIPE)
		(result, error) = ProcessOutput.communicate()
		Out = result.decode("utf-8")

		if(Out.startswith("Ping request could not find host") or "Request timed out" in Out):
			# IP is unreachable

			# Knowing what IP to show
			
			# print(len(IPNumberOfDots)-1)

			if(len(IPNumberOfDots)-1 == 3):
				# Normal scenario
				cprint(IP + " is unreachable", 'red')
			if(len(IPNumberOfDots)-1 == 2):
				# This means user inputed a base IP like X.Y only
				# Pring will padd the baseIP with 0 such as X.Y.0
				cprint(IPNumberOfDots[0] + "." + IPNumberOfDots[1] +".0"+ "."+ IPNumberOfDots[2] + " is unreachable", 'red')
			
			if(len(IPNumberOfDots)-1 == 1):
				# This means user inputed a base IP like X. only
				# Pring will padd the baseIP with 0 such as X.0.0.
				cprint(IPNumberOfDots[0] + ".0.0." + IPNumberOfDots[1] +" is unreachable", 'red')
			
		else:
			# It is reachable
			# Knowing what IP to show
			IPNumberOfDots = IP.split(".")
			# print(len(IPNumberOfDots)-1)

			if(len(IPNumberOfDots)-1 == 3):
				# Normal scenario
				cprint(IP + " is reachable", 'green')
				
			if(len(IPNumberOfDots)-1 == 2):
				# This means user inputed a base IP like X.Y only
				# Pring will padd the baseIP with 0 such as X.Y.0
				cprint(IPNumberOfDots[0] + "." + IPNumberOfDots[1] +".0"+ "."+ IPNumberOfDots[2] + " is reachable", 'green')
			
			if(len(IPNumberOfDots)-1 == 1):
				# This means user inputed a base IP like X. only
				# Pring will padd the baseIP with 0 such as X.0.0.
				cprint(IPNumberOfDots[0] + ".0.0." + IPNumberOfDots[1] +" is reachable", 'green')
		
main()
