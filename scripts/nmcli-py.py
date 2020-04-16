 ############################
# Toucom Technologies      #
# -------------------------#
# April 2020		   #
############################

# NMCLI using subprocess.py

import subprocess
import time
import sys

def isOpen(ap):
	if len(ap)>=2 and ap[2] == '':
			return True
	return False

def main():
	# device status (formatting output)
	out  = subprocess.run(['nmcli','--terse','dev'],stdout=subprocess.PIPE)
	lines = out.stdout.decode("utf-8").split('\n')
	#print(lines)
	wifi_interface = lines[1].split(":")
	state = wifi_interface[2]
	print("INTERFACE={} | STATE={}".format(wifi_interface[1],state))

	if state =='disconnected':
		# Force scan
		subprocess.run(['nmcli','dev','wifi','rescan'])
		# Get list of wifi networks
		p1 = subprocess.run(['nmcli','--terse','-f','SSID,SIGNAL,SECURITY','dev','wifi'], stdout=subprocess.PIPE)
		raw = p1.stdout.decode("utf-8").split('\n')
		print(raw)
		# filter for open actual ones (SSID can have --)
		aps = [ap.split(':') for ap in raw]
		# print(aps)
		open_aps = list(filter(isOpen, aps))
		print('[SSIDs Open Networks (SORTED)]')
		print(open_aps)
		if open_aps != []:
			# let's try to connect to the first one
			ssid = open_aps[0][0]
			#TODO: store connection UUID
			out = subprocess.run(['nmcli','dev','wifi','connect',ssid])
			# Connected?
			conn = False
			for i in range(5,0,-1):
				out  = subprocess.run(['nmcli','--terse','dev'],stdout=subprocess.PIPE)
				lines = out.stdout.decode("utf-8").split('\n')
				#print(lines)
				state = lines[1].split(':')[2]
				if state == 'connected':
					conn = True
					break
				sys.stdout.write(str(i)+' ')
				sys.stdout.flush()
				time.sleep(1)
			if conn:
				print("Successfully connected to {}".format(ssid))
				for i in range(5,0,-1):
					sys.stdout.write(str(i)+' ')
					sys.stdout.flush()
					time.sleep(1)
				print()
				## CALL PUPPET ##
				print("---- RUNNING PUPPETEER ----")
				subprocess.run(['node','../pup/'])
				## ----------- ##

				#disconnect from network
				out = subprocess.run(['nmcli','dev','disconnect','wlan0'])
				# Remove connection profile
				# TODO: Use connection UUID instead
				out  = subprocess.run(['nmcli','conn','delete',ssid])
			else:
				print("Couldn't connect to {} or too slow".format(ssid))
# call main()

if __name__ == "__main__":
	main()
