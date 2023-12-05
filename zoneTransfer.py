#!/home/kali/.pyenv/shims/python3
import subprocess
import re
from termcolor import colored

def is_valid_domain(domain):
    # Use a regular expression to check if the domain has a valid format
    domain_regex = re.compile(
        r"^(?:(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,6}$",
        flags=re.IGNORECASE
    )
    return bool(domain_regex.match(domain))

def check_zone_transfer(domain):
    if not is_valid_domain(domain):
        print(colored("Error: Please enter a valid domain.", 'red'))
        return

    try:
        ns_command = f"dig +short ns {domain}"
        ns_output = subprocess.check_output(ns_command, shell=True, text=True).strip().split('\n')

        if not ns_output:
            print(f"No nameservers found for {domain}")
            return

        vulnerable_servers = []
        for ns in ns_output:
            zone_transfer_command = f"dig axfr @{ns} {domain}"
            try:
                zone_transfer_output = subprocess.check_output(zone_transfer_command, shell=True, text=True)
                if "Transfer failed" not in zone_transfer_output:
                    vulnerable_servers.append(ns)
                    print(colored(f"Zone transfer successful for {ns}:", 'green'))
                    print(zone_transfer_output)
                else:
                    print(colored(f"Zone transfer failed for {ns}.", 'red'))
            except subprocess.CalledProcessError as e:
                pass  

        if vulnerable_servers:
            print(colored(f"The domain {domain} is vulnerable to zone transfer attacks.", 'red'))
            print("Vulnerable nameservers:")
            for vulnerable_ns in vulnerable_servers:
                print(colored(vulnerable_ns, 'yellow'))
        else:
            print(colored(f"The domain {domain} is not vulnerable to zone transfer attacks.", 'green'))

    except KeyboardInterrupt:
        print("\nCTRL+C detected. Exiting gracefully.")

if __name__ == "__main__":
    domain = input("Enter the domain: ")
    check_zone_transfer(domain)
