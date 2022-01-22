import os
import re
import sys


with open("infovol.txt", "w+") as file:
	profiles_list = []

	os.system(f"vol.py -f {sys.argv[1]} imageinfo > infovol.txt")
	for line in file:
		profiles = line
		profiles_list = re.findall('[W]\w+', profiles)
		break


with open("hivevol.txt", "w+") as file:
	addresses_list = []

	os.system(f"vol.py -f {sys.argv[1]} hivelist --profile={profiles_list[0]} > hivevol.txt")

	for line in file:
		if "\REGISTRY\MACHINE\SYSTEM" in line:
			addresses_list.append(line.split(' ')[:1])

		if "\SystemRoot\System32\Config\SAM" in line:
			addresses_list.append(line.split(' ')[:1])

os.system(f"vol.py -f {sys.argv[1]} --profile={profiles_list[0]} hashdump -y {' '.join(addresses_list[0])} -s {' '.join(addresses_list[1])} > hashes.txt")

os.system(f"john --format=NT --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt")
os.remove("hivevol.txt")
os.remove("infovol.txt")
