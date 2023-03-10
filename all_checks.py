#!/usr/bin/env python3
import os
import sys
import shutil
# Testing rebase another example
import socket
import psutil


def check_reboot():
    '''Returns True if the computer has a pending reboot.'''
    return os.path.exists('/run/reboot-required')

def check_disk_full(disk, min_gb, min_percent):
    '''Return True if there us not enough disk space, False otherwise.'''
    du = shutil.disk_usage(disk)
    # Calculate the percentage of free space
    percent_free = 100 * du.free / du.total
    gigabytes_free = du.free / 2**30
    if percent_free < min_percent or gigabytes_free < min_gb:
        return True
    return False


def check_root_full():
    '''Return True if the root partition is full, False otherwise.'''
    return check_disk_full(disk='/', min_gb=2, min_percent=10)

def check_no_network():
    '''Return True if it fails to resolve Google URL, False otherwise'''
    try:
        socket.gethostbyname('www.google.com')
        return False
    except:
        return True

def main():
    checks=[
        (check_reboot, 'Pending reboot'),
        (check_root_full, 'Root partition full'),
        (check_no_network, 'No working network'),   
    ]
    everything_ok = True
    for check, msg in checks:
        if check():
            print(msg)
            everything_ok = False
    if not everything_ok:
        sys.exit(1)

        
    print('Everything is ok.')
    sys.exit(0)

    
main()
