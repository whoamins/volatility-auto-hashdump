import os
import sys
import re

os.system("mkdir output_volatility")
os.system(f"volatility_2.6_lin64_standalone -f {sys.argv[1]} imageinfo > output_volatility/infovol.txt")

with open("output_volatility/infovol.txt", "r") as file:
	for line in file:
		profiles = line
		profiles_list = re.findall('[W]\w+', profiles)
		break


os.system(f"volatility_2.6_lin64_standalone -f {sys.argv[1]} hivelist --profile={profiles_list[0]} > output_volatility/hivevol.txt")


with open("output_volatility/hivevol.txt", "r") as file:
	addresses_list = []

	for line in file:
		if "\REGISTRY\MACHINE\SYSTEM" in line:
			addresses_list.append(line.split(' ')[:1])

		if "\SystemRoot\System32\Config\SAM" in line:
			addresses_list.append(line.split(' ')[:1])


os.system(f"volatility_2.6_lin64_standalone -f {sys.argv[1]} --profile={profiles_list[0]} hashdump -y {' '.join(addresses_list[0])} -s {' '.join(addresses_list[1])} > output_volatility/hashes.txt")

os.system(f"john --format=NT --wordlist=/usr/share/wordlists/rockyou.txt output_volatility/hashes.txt")
