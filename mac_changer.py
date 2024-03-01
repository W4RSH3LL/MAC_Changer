#!/usr/bin/env python

import subprocess
import optparse
import re
from colorama import Fore, Style

# Get arguments + options from the user
def get_args():
    parser = optparse.OptionParser() # Creating parser objects
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change the MAC address") # Adding interface options to the parser object
    parser.add_option("-m", "--mac", dest="new_mac", help="The new MAC address to assign") # Adding MAC Address options to the parser object
    (options, arguments) =  parser.parse_args() # Returning Options & Arguments

    # Verifying for user input
    if not options.interface:
        # Handle error
        parser.error(Fore.RED + "[-] Please enter an interface to change, use -h for more info [-]")
    elif not options.interface:
        # Handle error
        parser.error(Fore.RED + "[-] Please enter a MAC address to assign, use -h for more info [-]")
    else:
        return options # Returning the options and arguments from the parser

# Executing ifconfig commands to change MAC
def change_mac(interface, new_mac):
    print(Fore.CYAN + f'[+] Changing MAC address for: {interface}, assigning MAC address: {new_mac} [+]') # Giving Output for User
    subprocess.call(['ifconfig', interface, 'down']) # Turning off the interface
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac]) # Changing MAC Address of Interface
    subprocess.call(['ifconfig', interface, 'up']) # Turning on the interface

# Grabbing the new ether from ifconfig
def get_current_mac_address(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    ifconfig_result = ifconfig_result.decode('utf-8')  # Decode bytes to string

    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result) # Searching for the ether part inside ifconfig

    # Printing out the ether from ifconfig
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print(Fore.RED + "[-] Failed to read MAC address [-]")

# Comparing the current MAC with the ether from ifconfig
def verify_new_mac():
    options = get_args() # Calling the get_args func

    current_mac = get_current_mac_address(options.interface)
    print(Fore.YELLOW + f'[*] Current MAC = {current_mac} [*]')
    change_mac(options.interface, options.new_mac) # Calling change_mac func with args interface and new_mac

    current_mac = get_current_mac_address(options.interface)

    if current_mac == options.new_mac:
        # Success Messge
        print(Fore.GREEN + Style.BRIGHT + f'[+] MAC address has successfully been changed to: {current_mac} [+]')
        return 0
    else:
        # Error Message
        print(Fore.RED + f'[-] An error occured. Please use -h for more info... [-]')
        return 1

# Calling the main function
if __name__ == "__main__":
    verify_new_mac()
