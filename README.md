# Sony Bravia TV - Domoticz Python plugin
**Domoticz Python plugin for Sony Bravia TV**

*This plugin uses the [Sony Bravia RC API](https://github.com/aparraga/braviarc) by Antonio Parraga Navarro.
Also a lot of inspiration came from this [post](http://www.domoticz.com/forum/viewtopic.php?f=61&t=8301) by StefanPuntNL.*

## Table of Contents
- [Information](#information)
- [Sony Bravia plugin instructions](#sony-bravia-plugin-instructions)
  - [TV settings](#tv-settings)
  - [Domoticz settings](#domoticz-settings)
- [Screenshots](#screenshots)
- [Testing the plugin](#testing-the-plugin)
- [Confirmed working on the following TV´s](#confirmed-working-on-the-following-tvs)

## Information
The plugin will show information from your Sony Bravia TV in Domoticz.
It will work on Sony Bravia models 2013 and newer. Also tested on Sony Bravia X8509C and 55SD8505 with Android.
(Although not sure yet it will work on all Android TV's, maybe some models need simple IP control.)

**Information on the TV channel and program are only showed when you use the built-in TV tuner. Otherwise for example HDMI1 will be shown.**

**The volume slides shows the volume of the built-in speakers. If you have an amplifier attached to your TV, that volume is not shown.**
*You can use the on/off button of the slider switch though to mute/unmute the TV, also if you have the TV connected to an amplifier.*

**The remote control in the Status switch gives some extra options. See the screenshot below for extra info on some of the buttons.**

## Sony Bravia plugin instructions
Works with Pre-Shared Key (PSK). The default PSK you can use is 'sony', but you can change the PSK to something else. If you change it, remember to also change the PSK in the Domoticz hardware page.

### TV settings
* Enable remote start on your TV: [Settings] => [Network] => [Home Network Setup] => [Remote Start] => [On]

* Enable pre-shared key on your TV: [Settings] => [Network] => [Home Network Setup] => [IP Control] => [Authentication] => [Normal and Pre-Shared Key]

* Set pre-shared key on your TV: [Settings] => [Network] => [Home Network Setup] => [IP Control] => [Pre-Shared Key] => sony

* Give your TV a static IP address, or make a DHCP reservation for a specific IP address in your router.

* Determine the MAC address of your TV: [Settings] => [Network] => [Network Setup] => [View Network Status]

The IP address, PSK and MAC address need to be entered in the Domoticz hardware page, see screenshot below.

### Domoticz settings
See this [link](https://www.domoticz.com/wiki/Using_Python_plugins) for more information on the Domoticz plugins.
This plugin works with the old and new version of the Python framework in Domoticz.
* SSH to your server on which Domoticz is installed

* Enter the following commands
```bash
cd domoticz/plugins
git clone https://github.com/gerard33/sony-bravia.git
```
  * *When updating to the latest version on Github enter the following commands*
  ```bash
  cd domoticz/plugins/sony-bravia
  git pull
  ```

* Restart the Domoticz service
```bash
sudo service domoticz.sh restart
```

* Now go to **Setup**, **Hardware** in your Domoticz interface. There you add
**Sony Bravia TV**.

Make sure you enter all the required fields.

| Field | Information|
| ----- | ---------- |
| IP address | Enter the IP address of your TV (see instructions above how to find the IP address, also make sure it is static) |
| Pre-shared key | Enter the Pre-shared key here (default is sony) |
| MAC address | Enter the MAC address of your TV (see instructions above how to find the MAC address) |
| Volume bar | Option to enable or disable a Domoticz device for the volume bar, this can be used to control the volume of the TV, but only for the built-in speakers of the TV |
| Update interval | Enter the update interval in seconds, this determines with which interval the plugin polls the TV (must be between 10 and 30 seconds) |
| Debug | When set to true the plugin shows additional information in the Domoticz log |

After clicking on the Add button the devices are available in the **Switches** tab.

## Screenshots
![tv](https://cloud.githubusercontent.com/assets/11230573/25202175/bc1c9db8-2554-11e7-9a0f-39d182c700f5.png)
![tv2](https://cloud.githubusercontent.com/assets/11230573/25202176/bc332e0c-2554-11e7-821d-bd76c58f7bf1.png)

![sony_tv_control_channel](https://cloud.githubusercontent.com/assets/11230573/25483849/d0a9b4c4-2b57-11e7-9875-193567029e3b.png)

![tv3](https://cloud.githubusercontent.com/assets/11230573/25202177/bc3f921e-2554-11e7-842c-96c863f210dc.png)

![tvhw](https://cloud.githubusercontent.com/assets/11230573/25202178/bcfb2998-2554-11e7-80ec-9b2e85ee59f4.png)

![remote_functions](https://cloud.githubusercontent.com/assets/11230573/25874696/faddb72a-3513-11e7-9a43-f658de2eec4c.png)

## Testing the plugin
To do some easy testing with the plugin there is a `localtest.py` script that can be run from the command line.
Make sure you enter the IP address and PSK of your TV in `localtest.py` before executing it.
After that you can check if your TV works with the plugin.

```bash
cd domoticz/plugins/sony-bravia
./localtest.py
```

This will print some information regarding the TV to the console.

Thanks to ffes for `localtest.py` which is part of his [Buienradar](https://github.com/ffes/domoticz-buienradar) Python script.

## Confirmed working on the following TV´s
* KDL-50W829B

* KDL-42W705B

* KDL-55W805C

* KD-55X9005B

* KDL-42W805A --> with the use of cookies, check [this](http://www.domoticz.com/forum/viewtopic.php?f=65&t=16910&p=128866#p128866) for more information

* KD-49XD8305 Android

* KD-55X8509C Android

* KD-55SD8505 Android

* KD-55XD8505 Android

* KDL-50W755c Android
