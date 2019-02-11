import subprocess
import os
import sys
import socket
from datetime import date


def get_filename_datetime():
    return ' ' + str(date.today())

def create_directory(domain, name):
    subdomain_directory = 'Reports/' + domain + name + '/subdomains'
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
        ip_address = socket.gethostbyname(domain)

        if ip_address:
            print ("\n[+] Running Knockpy:\n")
            proc = subprocess.Popen(["python","Tools/knock/knockpy/knockpy.py","-c",
                    domain],stdout=subprocess.PIPE)
            knockpyResult = handle_output(proc)

            print ("\n[+] Running Sublist3r:\n")
            sublist3r_file = 'Reports/' + domain + name + '/subdomains/sublist3r.txt'
            proc = subprocess.Popen(["python","Tools/Sublist3r/sublist3r.py","-d",
                    domain,"-o", sublist3r_file],stdout=subprocess.PIPE)
            sublist3rResult = handle_output(proc)

            return {"Knockpy": knockpyResult, "Sublist3r": sublist3rResult}
    except Exception,e:
        print ("\n[!] Subdomain Discovery Failed: " + str(e) + "\n")
        return ""


def main():
    print ("AJRECON")
    print ("Bros you go like relax small\n")

    if len(sys.argv) != 2:
		print ("\n[+] Usage: %s <domain name>\n" % sys.argv[0])
		sys.exit(1)

    domain = sys.argv[1]
    name = get_filename_datetime()

    create_directory(domain, name)
    subdisResult = subdis(domain, name)


if __name__ == '__main__':
    main()
