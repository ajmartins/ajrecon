#!/usr/bin/python
import subprocess
import os
import sys
from datetime import date


def get_filename_datetime():
    return ' ' + str(date.today())

def create_directory(domain, name):
    subdomain_directory = 'Reports/' + domain + name
    if not os.path.isdir(subdomain_directory):
        os.makedirs(subdomain_directory)

# Takes a piped process started by subprocess.Popen and directs its
# output both to sys.stdout and to a string variable.
def handle_output(proc):
    output = ""
    while proc.poll() is None:
        outputline = proc.stdout.readline()
        output += outputline
        sys.stdout.write(outputline)
    outputline = proc.stdout.read()
    output += outputline
    sys.stdout.write(outputline)
    sys.stdout.flush()
    return output

# Subdomain Discovery.
def subdis(domain, name):
    print ("#####################################"
		  + "\nSUBDOMAIN DISCOVERY"
		  + "\n#####################################"
		  + "\nBeginning Subdomain Enumeration. This may take a few minutes.\n")
    try:
        print ("\n[+] Running Sublist3r:\n")
        subdomains_file = 'Reports/' + domain + name + '/subdomains.txt'
        proc = subprocess.Popen(["python","Tools/Sublist3r/sublist3r.py","-d",
                domain,"-o", subdomains_file],stdout=subprocess.PIPE)
        sublist3rResult = handle_output(proc)
        return {"Sublist3r": sublist3rResult}

    except Exception,e:
        print ("\n[!] Subdomain Discovery Failed: " + str(e) + "\n")
        return ""

# Finding New Endpoints/JS Files[Domain].
def newendpoints(domain, name):
    print ("#####################################"
		  + "\nFINDING NEW ENDPOINTS"
		  + "\n#####################################"
		  + "\nChecking for Endpoints. This may take a few minutes.\n")
    try:
        print ("\n[+] Running LinkFinder:\n")
        endpoints_file = 'Reports/' + domain + name + '/endpoints.html'
        proc = subprocess.Popen(["python","Tools/LinkFinder/linkfinder.py","-i",
                "https://"+domain,"-d","-o",endpoints_file],stdout=subprocess.PIPE)
        LinkFinderResult = handle_output(proc)

        return {"LinkFinder": LinkFinderResult}
    except Exception,e:
        print ("\n[!] Finding New Endpoints Failed: " + str(e) + "\n")
        return ""

# Go Back In Time[Domain].
def gobackintime(domain):
    print ("#####################################"
		  + "\nFINDING JS FILES"
		  + "\n#####################################"
		  + "\nChecking for JS Files. This may take a few minutes.\n")
    try:
        print ("\n[+] Running WayBackUrls:\n")
        proc = subprocess.Popen(["waybackurls",domain,"| uniq | sort"],stdout=subprocess.PIPE)
        WayBackUrlsResult = handle_output(proc)

        return {"WayBackUrls": WayBackUrlsResult}
    except Exception,e:
        print ("\n[!] Finding JS Files Failed: " + str(e) + "\n")
        return ""

# Screenshots[Subdomains].
def screenshots(domain, name):
    print ("#####################################"
		  + "\nTAKING SCREENSHOTS"
		  + "\n#####################################"
		  + "\nTaking Screenshots for Validation. This may take a few minutes.\n")
    try:
        print ("\n[+] Running WebScreenshot:\n")
        subdomains_file = 'Reports/' + domain + name + '/subdomains.txt'
        screenshots_files = 'Reports/' + domain + name + '/Screenshots/'
        proc = subprocess.Popen(["python","Tools/webscreenshot/webscreenshot.py",
                "-i",subdomains_file,"-o",screenshots_files],stdout=subprocess.PIPE)
        WebScreenshotResult = handle_output(proc)

        return {"WebScreenshot": WebScreenshotResult}
    except Exception,e:
        print ("\n[!]Taking Screenshots Failed: " + str(e) + "\n")
        return ""

# Content Discovery[Subdomains].
def contentdis(domain, name):
    print ("#####################################"
		  + "\nCHECKING FOR COMMON FILES/DIRECTORIES"
		  + "\n#####################################"
		  + "\nBruteforcing for Files/Directories. This will definitely take more than a few minutes.\n")
    try:
        print ("\n[+] Running Dirsearch:\n")
        subdomains_file = 'Reports/' + domain + name + '/subdomains.txt'
        contentdis_file = 'Reports/' + domain + name + '/contentdiscovery.txt'
        proc = subprocess.Popen(["python3","Tools/dirsearch/dirsearch.py", "-e","txt",
                "-L",subdomains_file,"--plain-text-report="+contentdis_file],stdout=subprocess.PIPE)
        DirsearchResult = handle_output(proc)

        return {"Dirsearch": DirsearchResult}
    except Exception,e:
        print ("\n[!]Content Discovery Failed: " + str(e) + "\n")
        return ""

# portscan
# PossibleVulnScan= Cors, SubdomainTakeover,AWS/Github etc.


def main():
    print ("AJRECON")
    print ("Sit back and Relax\n")

    if len(sys.argv) != 2:
		print ("\n[+] Usage: %s <domain name>\n" % sys.argv[0])
		sys.exit(1)

    domain = sys.argv[1]
    name = get_filename_datetime()

    create_directory(domain, name)
    subdisResult = subdis(domain, name)
    newendResult = newendpoints(domain, name)
    jsfileResult = gobackintime(domain)
    webscreensht = screenshots(domain, name)
    condisResult = contentdis(domain, name)


if __name__ == '__main__':
    main()
