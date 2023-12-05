# Zone Transfer Checker

# Disclaimer
Use this script responsibly and only on systems for which you have explicit authorization. Unauthorized testing could lead to legal consequences. The author assumes no liability and is not responsible for any misuse of this script.
This Python script checks if a domain is vulnerable to zone transfer attacks. It retrieves the authoritative nameservers for the specified domain and attempts a zone transfer attack for each of them.

## Installation

1. Install the required dependencies by running the following command:

   ```bash
   pip install -r requirements.txt
