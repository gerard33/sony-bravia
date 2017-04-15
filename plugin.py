#       
#       Sony Bravia Plugin
#       Author: G3rard, 2017
#       
"""
<plugin key="sony" name="Sony Bravia TV" author="G3rard" version="0.3" wikilink="https://github.com/gerard33/sony-bravia" externallink="https://www.sony.com/electronics/bravia">
    <description>
Sony Bravia plugin.<br/><br/>
It will work on Sony Bravia models 2013 and newer. Not tested on Sony Bravia with Android yet!<br/>
Works with pre-shared key.<br/><br/>
Prerequisites:<br/>
* Enable remote start on your TV: [Settings] => [Network] => [Home Network Setup] => [Remote Start] => [On]<br/>
* Enable pre-shared key on your TV: [Settings] => [Network] => [Home Network Setup] => [IP Control] => [Authentication] => [Normal and Pre-Shared Key]<br/>
* Set pre-shared key on your TV: [Settings] => [Network] => [Home Network Setup] => [IP Control] => [Pre-Shared Key] => sony<br/>
* Give your TV a static IP address, or make a DHCP reservation for a specific IP address in your router.<br/>
* Determine the MAC address of your TV: [Settings] => [Network] => [Network Setup] => [View Network Status]<br/>
    </description>
    <params>
        <param field="Address" label="IP address" width="200px" required="true" default="192.168.1.191"/>
        <param field="Mode1" label="Pre-shared key (PSK)" width="200px" required="true" default="sony"/>
        <param field="Mode2" label="MAC address" width="200px" required="true" default="AA:BB:CC:DD:EE:FF"/>
        <param field="Mode3" label="Volume bar" width="75px">
            <options>
                <option label="True" value="Volume"/>
                <option label="False" value="Fixed" default="true" />
            </options>
        </param>
        <param field="Mode5" label="Update interval (sec)" width="30px" required="true" default="30"/>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal" default="true" />
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz
import datetime

from bravia import BraviaRC

class BasePlugin:
    isConnected = False
    powerOn = False
    tvState = 0
    tvVolume = 0
    tvSource = 0
    tvPlaying = {} #''
    startTime = ''
    endTime = ''
    perc_playingTime = 0
    _tv = None
    
    # Executed once at reboot/update, can create up to 255 devices
    def onStart(self):
        global _tv
        
        if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(1)
        
        _tv = BraviaRC(Parameters["Address"], Parameters["Mode1"], Parameters["Mode2"]) #IP, PSK, MAC
        
        Options =   {   "LevelActions"  :"|||||" , 
                        "LevelNames"    :"Off|TV|HDMI1|HDMI2|HDMI3|HDMI4" ,
                        "LevelOffHidden":"true",
                        "SelectorStyle" :"0"
                     }
        
        if (len(Devices) == 0):
            Domoticz.Device(Name="Status", Unit=1, Type=17, Image=2, Switchtype=17).Create()
            if Parameters["Mode3"] == "Volume":
                Domoticz.Device(Name="Volume", Unit=2, Type=244, Subtype=73, Switchtype=7, Image=8).Create()
            Domoticz.Device(Name="Source", Unit=3, TypeName="Selector Switch", Switchtype=18, Image=2, Options=Options).Create()
            Domoticz.Log("Devices created")
        elif (Parameters["Mode3"] == "Volume" and 2 not in Devices):
            Domoticz.Device(Name="Volume", Unit=2, Type=244, Subtype=73, Switchtype=7, Image=8).Create()
            Domoticz.Log("Volume device created.")
        elif (Parameters["Mode3"] != "Volume" and 2 in Devices):
            Devices[2].Delete()
            Domoticz.Log("Volume device deleted.")
        else:
            if (1 in Devices):
                self.tvState = Devices[1].nValue
            if (2 in Devices):
                self.tvVolume = Devices[2].nValue
            if (3 in Devices):
                self.tvSource = Devices[3].nValue
        
        # Set update interval, values below 10 seconds are not allowed due to timeout of 5 seconds in bravia.py script
        updateInterval = int(Parameters["Mode5"])
        if updateInterval < 30:
            if updateInterval < 10:
                updateInterval == 10
            Domoticz.Log("Update interval set to " + str(updateInterval) + " (minimum is 10 seconds)")
            Domoticz.Heartbeat(updateInterval)
        else:
            Domoticz.Heartbeat(30)
        
        DumpConfigToLog()

        return #--> return True

    def onConnect(self, Status, Description):
        if (Status == 0):
            self.isConnected = True
            Domoticz.Log("Connected successfully to: "+Parameters["Address"])
        else:
            self.isConnected = False
            self.powerOn = False
            Domoticz.Log("Failed to connect ("+str(Status)+") to: "+Parameters["Address"])
            Domoticz.Debug("Failed to connect ("+str(Status)+") to: "+Parameters["Address"]+" with error: "+Description)
            self.SyncDevices()
        return
    
    # Called when a single,complete message is received from the external hardware
    def onMessage(self, Data, Status, Extra):
        Domoticz.Log('onMessage: '+str(Data)+" ,"+str(Status)+" ,"+str(Extra))    
        return True
    
    # Executed each time we click on device through Domoticz GUI
    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

        Command = Command.strip()
        action, sep, params = Command.partition(' ')
        action = action.capitalize()
        params = params.capitalize()
       
        if self.powerOn == False:
            if Unit == 1:     # TV power switch
                if action == "On":
                    if (Parameters["Mode2"] == ""):
                        Domoticz.Error("TV can not be turned on as there is no MAC address configured")
                    else:
                        _tv.turn_on()
                        self.tvPlaying = "TV starting" # Show that the TV is starting, as booting the TV takes some time
                        #self.tvSource = "10"
                        self.SyncDevices()
        else:
            if Unit == 1:     # TV power switch
                if action == "Off":
                    _tv.turn_off()
                    self.tvPlaying = "Off"
                    self.tvSource = "0"
                    self.SyncDevices()
                
            if Unit == 2:     # TV volume
                if action == 'Set': #--> and (params.capitalize() == 'Level') or (Command.lower() == 'Volume')
                    self.tvVolume = str(Level)
                    _tv.set_volume_level(self.tvVolume)
                elif action == "Off":
                    _tv.mute_volume()
                    UpdateDevice(2, 0, str(self.tvVolume))
                elif action == "On":
                    _tv.mute_volume()
                    UpdateDevice(2, 1, str(self.tvVolume))
                    
            if Unit == 3:   # TV source
                if Command == 'Set Level':
                    if Level == 10:
                        _tv.send_req_ircc("AAAAAQAAAAEAAAAAAw==") #TV Num1
                        self.GetTVInfo()
                    if Level == 20:
                        _tv.send_req_ircc("AAAAAgAAABoAAABaAw==") #HDMI1
                        self.tvPlaying = "HDMI 1"
                        self.tvSource = "20"
                        self.SyncDevices()
                    if Level == 30:
                        _tv.send_req_ircc("AAAAAgAAABoAAABbAw==") #HDMI2
                        self.tvPlaying = "HDMI 2"
                        self.tvSource = "30"
                        self.SyncDevices()
                    if Level == 40:
                        _tv.send_req_ircc("AAAAAgAAABoAAABcAw==") #HDMI3
                        self.tvPlaying = "HDMI 3"
                        self.tvSource = "40"
                        self.SyncDevices()
                    if Level == 50:
                        _tv.send_req_ircc("AAAAAgAAABoAAABdAw==") #HDMI4
                        self.tvPlaying = "HDMI 4"
                        self.tvSource = "50"
                        self.SyncDevices()
        
        return

    def onDisconnect(self):
        self.isConnected = False
        Domoticz.Log("Sony Bravia TV has disconnected.")
        return
        
    # Executed once when HW updated/removed
    def onStop():
        Domoticz.Log("onStop called")
        return True
    
    # Execution depend of Domoticz.Heartbeat(x) x in seconds
    def onHeartbeat(self):
        try:
            tvStatus = _tv.get_power_status()
            Domoticz.Debug('Status TV: ' + tvStatus)
        #except KeyError:
        except Exception as err:
            Domoticz.Log('Not connected to TV (' +  err + ')')

        if tvStatus == 'active':
            self.powerOn = True
            self.GetTVInfo()
        else:
            self.powerOn = False
            self.SyncDevices()

        return

    def SyncDevices(self):
        if self.powerOn == False:
            if self.tvPlaying == "TV starting":         # TV is booting and not yet responding to get_power_status
                UpdateDevice(1, 1, self.tvPlaying)
                #UpdateDevice(3, 1, self.tvSource)
            else:                                       # TV is off so set devices to off
                UpdateDevice(1, 0, "Off")
                if Parameters["Mode3"] == "Volume":
                    UpdateDevice(2, 0, str(self.tvVolume))
                UpdateDevice(3, 0, "0")
        else:
            if self.tvPlaying == "Off":                 # TV is set to off in Domoticz, but self.powerOn is still true
                UpdateDevice(1, 0, self.tvPlaying)
                if Parameters["Mode3"] == "Volume":
                    UpdateDevice(2, 0, str(self.tvVolume))
                UpdateDevice(3, 0, self.tvSource)
            else:                                       # TV is on so set devices to on
                UpdateDevice(1, 1, self.tvPlaying)
                if Parameters["Mode3"] == "Volume":
                    UpdateDevice(2, 2, str(self.tvVolume))
                UpdateDevice(3, 1, self.tvSource)

        return
    
    def GetTVInfo(self):
        self.tvPlaying = _tv.get_playing_info()
        if not self.tvPlaying:  # Dict is empty
            Domoticz.Debug("No information from TV received (maybe TV is paused)")
        else:
            if self.tvPlaying['programTitle'] != None:      # Get information on channel and program title if tuner of TV is used
                if self.tvPlaying['startDateTime'] != None: # Show start time and end time of program
                    self.startTime, self.endTime, self.perc_playingTime = _tv.playing_time(self.tvPlaying['startDateTime'], self.tvPlaying['durationSec'])
                    self.tvPlaying = (self.tvPlaying['title'] + ' - ' + self.tvPlaying['programTitle'] + ' [' + str(self.startTime) + ' - ' + str(self.endTime) +']')
                    Domoticz.Debug("Program information: " + str(self.startTime) + "-" + str(self.endTime) + " [" + str(self.perc_playingTime) + "%]")
                else:
                    self.tvPlaying = str((self.tvPlaying['title'] + ' - ' + self.tvPlaying['programTitle']))
                UpdateDevice(1, 1, self.tvPlaying)
                UpdateDevice(3, 1, "10")        # Set source device to TV
            else:                               # No program info found
                self.tvPlaying = self.tvPlaying['title']
                if "/MHL" in self.tvPlaying:    # Source contains /MHL, that can be removed
                    self.tvPlaying = self.tvPlaying.replace("/MHL", "")
                UpdateDevice(1, 1, self.tvPlaying)
                if "HDMI 1" in self.tvPlaying:
                    UpdateDevice(3, 1, "20")    # Set source device to HDMI1
                elif "HDMI 2" in self.tvPlaying:
                    UpdateDevice(3, 1, "30")    # Set source device to HDMI2
                elif "HDMI 3" in self.tvPlaying:
                    UpdateDevice(3, 1, "40")    # Set source device to HDMI3
                elif "HDMI 4" in self.tvPlaying:
                    UpdateDevice(3, 1, "50")    # Set source device to HDMI4
            
            # Get volume information of TV
            if Parameters["Mode3"] == "Volume":
                self.tvVolume = _tv.get_volume_info()
                self.tvVolume = self.tvVolume['volume']
                if self.tvVolume != None:
                    UpdateDevice(2, 2, str(self.tvVolume))
    
_plugin = BasePlugin()

def onStart():
    _plugin.onStart()

def onConnect(Status, Description):
    _plugin.onConnect(Status, Description)

def onMessage(Data, Status, Extra):
    _plugin.onMessage(Data, Status, Extra)

def onCommand(Unit, Command, Level, Hue):
    _plugin.onCommand(Unit, Command, Level, Hue)

def onDisconnect():
    _plugin.onDisconnect()

def onHeartbeat():
    _plugin.onHeartbeat()

# Update Device into database
def UpdateDevice(Unit, nValue, sValue, AlwaysUpdate=False):
    # Make sure that the Domoticz device still exists (they can be deleted) before updating it 
    if (Unit in Devices):
        if ((Devices[Unit].nValue != nValue) or (Devices[Unit].sValue != sValue) or (AlwaysUpdate == True)):
            Devices[Unit].Update(nValue, str(sValue))
            Domoticz.Log("Update "+str(nValue)+":'"+str(sValue)+"' ("+Devices[Unit].Name+")")
    return

# Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Internal ID:     '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("External ID:     '" + str(Devices[x].DeviceID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
