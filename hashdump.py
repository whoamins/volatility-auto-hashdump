import os
import sys
import re


with open("infovol.txt", "w+") as file:
	profiles_list = []

	try:
		os.system(f"volatility_2.6_lin64_standalone -f {sys.argv[1]} imageinfo > infovol.txt")
	except:
		print("Maybe you forgot to export PATH to your Volatility")
		sys.exit()

	for line in file:
		profiles = line
		profiles_list = re.findall('[W]\w+', profiles)
		break


with open("hivevol.txt", "w+") as file:
	addresses_list = []

	try:
		os.system(f"volatility_2.6_lin64_standalone -f {sys.argv[1]} hivelist --profile={profiles_list[0]} > hivevol.txt")
	except:
		print("Maybe you forgot to export PATH to your Volatility")
		sys.exit()

	for line in file:
		if "\REGISTRY\MACHINE\SYSTEM" in line:
			addresses_list.append(line.split(' ')[:1])

		if "\SystemRoot\System32\Config\SAM" in line:
			addresses_list.append(line.split(' ')[:1])

try:
	os.system(f"volatility_2.6_lin64_standalone -f {sys.argv[1]} --profile={profiles_list[0]} hashdump -y {' '.join(addresses_list[0])} -s {' '.join(addresses_list[1])} > hashes.txt")
except:
	print("Maybe you forgot to export PATH to your Volatility")
	sys.exit()


os.system(f"john --format=NT --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt")
