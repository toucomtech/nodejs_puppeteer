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
	state = None
	for i in lines:
		info = i.split(':')
		#print(info)
		if len(info)<1:
			break
		if info[1] == 'wifi':
			state = info[2]
			break
	print("INTERFACE=wifi | STATE={}".format(state))

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
			out = subprocess.run(['nmcli','dev','wifi','connect',ssid])
			# Connected?
			conn = False
			for i in range(5,0,-1):
				out  = subprocess.run(['nmcli','--terse','dev'],stdout=subprocess.PIPE)
				lines = out.stdout.decode("utf-8").split('\n')
				#print(lines)
				state = None
				for inter in lines:
					info = inter.split(':')
					#print(info)
					if len(info)<1:
						break
					if info[1] == 'wifi':
						state = info[2]
						break
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
				print('')
				#TODO: Remove, seems not to be working
				out = subprocess.run(['nmcli','network','connectivity','check'], stdout=subprocess.PIPE)
				ccnt = out.stdout.decode('utf-8').split('\n')[0]
				print('Connectivity [{}]'.format(ccnt))
				#if ccnt != 'full':
				#	print('Sending data... [MOCK]');
				#elif:
				## CALL PUPPET ##
				print("---- RUNNING PUPPETEER ----")
				# Will run index.js in /puppeteer
				subprocess.run(['node','./../'])
				## ----------- ##
				#disconnect from network
				out = subprocess.run(['nmcli','dev','disconnect','wlan0'])
				# Get WIFI connection UUID
				out = subprocess.run(['nmcli','--terse','-f','NAME,TYPE,UUID','conn','show'],stdout=subprocess.PIPE)
				lines = out.stdout.decode('utf-8').split('\n')
				for l in lines:
					con = l.split(':')
					if(con[1] == '802-11-wireless'):
						uuid = con[2]
						# Remove connection profile
						out  = subprocess.run(['nmcli','conn','delete',uuid])
			else:
				print("Couldn't connect to {} or too slow".format(ssid))
# call main()

if __name__ == "__main__":
	main()
