#!/usr/bin/python


import sys
import time
#import StringIO
#import commands
import re
import threading
import subprocess


#protect-ico proprietary Code
class Customer_Scanner(object):
    """A customer  with an Active Account. Customers have the
    following properties:

    Attributes:
        name: A string representing the customer's name.
        active: A Bool tracking the current status of the customer's account.
    """

    def __init__(self, name,domain, active=True):
        """Return a Customer object whose name is *name* and starting
        status is *active*.
        domain is there asset """
        self.name = name
        self.active = active
        self.domain = domain
        #just seems like having the location in the object  from getgo works just check each file after each step
        self.hosts_location_aquatone = "/root/aquatone/" + domain + "/hosts.json"
        self.open_ports_location = "/root/aquatone/" + domain + "/open_ports.txt"
        self.takeover_location =  "/root/aquatone/" + domain + "/takeovers.txt"
        self.total_takeovers = []





    def aquatone_scan(self,target):

        cmd = ['proxychains', 'aquatone-scan', '--threads', '25','--ports','huge', "--domain", target]
        print("\nRunning command: " + ' '.join(cmd))
        sp = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = ""
        while True:
            out = sp.stdout.read(1).decode('utf-8')
            if out == '' and sp.poll() != None:
                break
            if out != '':
                output += out
                sys.stdout.write(out)
                sys.stdout.flush()

        # Getting discovered ports from the masscan output and sorting them
        # results = re.findall('port (\d*)', output)
        if output:
            print(output)




    def discover(self,target):

        cmd = ['proxychains', 'aquatone-discover', '--threads', '25', "--domain",target]
        print("\nRunning command: " + ' '.join(cmd))
        sp = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = ""
        while True:
            out = sp.stdout.read(1).decode('utf-8')
            if out == '' and sp.poll() != None:
                break
            if out != '':
                output += out
                sys.stdout.write(out)
                sys.stdout.flush()

        # Getting discovered ports from the masscan output and sorting them
        # results = re.findall('port (\d*)', output)
        if output:
            print(output)





    def takeover(self, target):

        cmd = ['proxychains', 'aquatone-takeover', '--threads', '25',"--domain",target]
        print("\nRunning command: " + ' '.join(cmd))
        sp = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = ""
        while True:
            out = sp.stdout.read(1).decode('utf-8')
            if out == '' and sp.poll() != None:
                break
            if out != '':
                output += out
                sys.stdout.write(out)
                sys.stdout.flush()

        # Getting discovered ports from the masscan output and sorting them
        # results = re.findall('port (\d*)', output)
        if output:
            print(output)




    def scan_domain(self,target):


        cmd = ['proxychains', 'python3', 'photon.py', '--dns','--threads',"20",'-e','json','-o',target,'-u',target]
        print("\nRunning command: " + ' '.join(cmd))
        sp = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = ""
        while True:
            out = sp.stdout.read(1).decode('utf-8')
            if out == '' and sp.poll() != None:
                break
            if out != '':
                output += out
                sys.stdout.write(out)
                sys.stdout.flush()

        # Getting discovered ports from the masscan output and sorting them
        #results = re.findall('port (\d*)', output)
        if output:
            print(output)











def main():
    targets = open("seeds.txt","r")
    for target in targets:
        Customer_Object = Customer_Scanner("test", target.strip(), True)
        print("*" * 50)
        print("Performing Web Based Recon On Target")
        print("*" * 50)
        print(Customer_Object.name)
        print("*" * 50)
        print("Entering Url And SubDomain Discover Scan")
        print("*" * 50)
        try:
            result1 = Customer_Object.scan_domain(Customer_Object.domain)
        except:
            pass

        try:
            print("*" * 50)
            print("Discovering SubDomains on Target")
            print("*" * 50)
            result2 = Customer_Object.discover(Customer_Object.domain)
            print("*" * 50)
            print("Discovering Ports Open on Targets")
            print("*" * 50)
            result3 = Customer_Object.aquatone_scan(Customer_Object.domain)
            result4 = Customer_Object.takeover(Customer_Object.domain)
            print("*" * 50)
            print("Discovering Ports Open on Targets")
            print("*" * 50)
            hosts_out = open(Customer_Object.hosts_location_aquatone, "r")
            ports_open_out = open(Customer_Object.open_ports_location, "r")
            takeovers_out = open(Customer_Object.takeover_location, "r")
            print(Customer_Object.hosts_location_aquatone)
            for Data in hosts_out:
                print(Data.strip())

            print(Customer_Object.open_ports_location)
            for Data in ports_open_out:
                print(Data.strip())
            print(Customer_Object.takeover_location)
            for Data in takeovers_out:
                print(Data.strip())
                local_takeover = {"domain": Customer_Object.domain, "Takeover_Data": Data.strip()}
                Customer_Object.total_takeovers.append(local_takeover)
        except:
            pass

main()
