# Connect to the specified open networky
import NetworkManager
import uuid
import sys
import time
# TO RUN SHELL CMDs
import os
# SSID of Open Network
ssid = 'Pineapple_Open'
# Connection Name
name = 'Fireworks'
# Connection Object
new_connection = {
     '802-11-wireless': {'mode': 'infrastructure',
                         'ssid': ssid},
     'connection': {'id': name,
                    'type': '802-11-wireless',
                    'uuid': str(uuid.uuid4())},
     'ipv4': {'method': 'auto'},
     'ipv6': {'method': 'auto'}
}
# Add connection
NetworkManager.Settings.AddConnection(new_connection)
print("Connection "+name+" Added")
# Get Connection 
connections = NetworkManager.Settings.ListConnections()
connections = dict([(x.GetSettings()['connection']['id'], x) for x in connections])
conn = connections[name]
# Get Network Interfaces
devices = NetworkManager.NetworkManager.GetDevices()
# Get Wireless device
for dev in devices:
	if dev.DeviceType == NetworkManager.NM_DEVICE_TYPE_WIFI and dev.State == NetworkManager.NM_DEVICE_STATE_DISCONNECTED:
		break
# Activate a connection by name
NetworkManager.NetworkManager.ActivateConnection(conn,dev,"/")
# RUN SHELL AFTER ('subprocess' in next version to handle output)
print("Connection in progress...")
os.system('nmcli dev')
for i in xrange(10,0,-1):
    sys.stdout.write(str(i)+' ')
    sys.stdout.flush()
    time.sleep(1)
os.system('nmcli dev')
print('---- Connectivity ----')
os.system('nmcli networking connectivity')
print('Deleting Added Connection...')
os.system('nmcli conn delete '+name)