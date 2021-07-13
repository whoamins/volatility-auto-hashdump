import os
import sys
import re


os.system("touch infovol.txt && touch hivevol.txt")
os.system(f"volatility_2.6_lin64_standalone -f {sys.argv[1]} imageinfo > infovol.txt")

with open("infovol.txt", "r") as file:
	profiles_list = []

	for line in file:
		profiles = line
		profiles_list = re.findall('[W]\w+', profiles)
		break


try:
	os.system(f"volatility_2.6_lin64_standalone -f {sys.argv[1]} hivelist --profile={profiles_list[0]} > hivevol.txt")
except:
	print("Try to export PATH to your Volatility")
	sys.exit()

with open("hivevol.txt", "r") as file:
	addresses_list = []

	for line in file:
		if "\REGISTRY\MACHINE\SYSTEM" in line:
			addresses_list.append(line.split(' ')[:1])

		if "\SystemRoot\System32\Config\SAM" in line:
			addresses_list.append(line.split(' ')[:1])

try:
	os.system(f"volatility_2.6_lin64_standalone -f {sys.argv[1]} --profile={profiles_list[0]} hashdump -y {' '.join(addresses_list[0])} -s {' '.join(addresses_list[1])} > hashes.txt")
except:
	print("Try to export PATH to your Volatility")
	sys.exit()

os.system(f"john --format=NT --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt")

os.system(f"rm hivevol.txt && rm infovol.txt")
