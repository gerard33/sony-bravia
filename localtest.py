#!/usr/bin/env python3
#
#   Sony Bravia - Domoticz Python plugin
#   G3rard
#
#   With thanks to Frank Fesevur for localtest
#
try:
    import Domoticz
except ImportError:
    import fakeDomoticz as Domoticz

import os
from bravia import BraviaRC
import sys

### Enter the IP address, PSK and MAC address of the TV below
ip = '192.168.1.191'
psk = 'sony'
mac = 'AA:BB:CC:DD:EE:FF'
###

x = BraviaRC(ip, psk, mac)

try:
    tvstatus = x.get_power_status()
    #print('Status TV:', tvstatus)
except KeyError:
    print('TV not found')
    sys.exit()

if tvstatus == 'active':
    #zet op NLD1
    #NLD1 = x.send_req_ircc(HOST, PSK, 'AAAAAQAAAAEAAAAAAw==')
    #NLD1 = x.send_req_ircc(x.get_command_code('Num1'))
    #print(NLD1)
    #zet op NLD2
    #NLD2 = x.send_req_ircc(HOST, PSK, 'AAAAAQAAAAEAAAABAw==')
    #NLD2 = x.send_req_ircc(x.get_command_code('Num2'))
    #print(NLD2)
    
    #go = x.send_req_ircc("AAAAAgAAABoAAABaAw==") #HDMI1
    
    tvplaying = x.get_playing_info()
    #print(tvplaying)
    if tvplaying['programTitle'] != None:
        print(tvplaying['title'], '-', tvplaying['programTitle'])
        starttime, endtime, perc_playingtime = x.playing_time(tvplaying['startDateTime'], tvplaying['durationSec'])
        print('Playing:', starttime, '-', endtime, '[' + str(perc_playingtime) + '%]')
    else:
        print('Playing:', tvplaying['title'])
    #get starttime (2017-03-24T00:00:00+0100) and calculate endtime based with duration (secs)

    #print(json.dumps(test, indent=2))
    tvinfo = x.get_system_info()
    print('TV model:', tvinfo['model'])
    #print(json.dumps(test2, indent=2))
    #test3 = get_network_info()
    
    network = x.get_network_info()
    print('MAC address:', network['mac'])
    #print(network)
    
    #test_vol = x.set_volume_level("20")
    #print(test_vol)
    
    vol = x.get_volume_info()
    print('Volume:', vol['volume'])
    
    #test_info = x.get_test_info()
    
    #test_mute = x.get_mute_info()
    #print(test_mute)
    
    #test = x.get_source('tv:dvbc')
    #print('Source list:', test)
    
    #test2= x.load_source_list()
    #print(test2)
    #test3 = x.select_source('HDMI 2')
    #print(test3)
    
else:
    print('TV status:', tvstatus) #status is standby net na het uitzetten, daarna niet meer bereikbaar
