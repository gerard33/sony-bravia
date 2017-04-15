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
It will work on Sony Bravia models 2013 and newer. Also tested on Sony Bravia X8509C with Android.
(Although not sure yet it will work on all Android TV's, maybe that needs simple IP control.)

**Information on the TV channel and program are only showed when you use the built-in TV tuner. Otherwise for example HDMI1 will be shown.**

**The volume slides shows the volume of the built-in speakers. If you have an amplifier attached to your TV, that volume is not shown.**
*You can use the on/off button of the slider though to mute/unmute the TV, also if you have the TV connected to an amplifier.*

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
* SSH to your server on which Domoticz is installed

* Enter the following commands
```bash
cd domoticz/plugins
git clone https://github.com/gerard33/sony-bravia.git
```
* Restart the Domoticz service
```bash
sudo service domoticz.sh restart
```

* Now go to **Setup**, **Hardware** in your Domoticz interface. There you add
**Sony Bravia TV**.

Make sure you enter all the required fields.
| Field | Information|
| ----- | ---- |
| IP address | Enter the IP address of your TV (see instructions above how to find the IP address, also make sure it is static) |
| Pre-shared key | Enter the Pre-shared key here (default is sony) |
| MAC address | Enter the MAC address of your TV (see instructions above how to find the MAC address) |
| Volume bar | Option to enable or disable a Domoticz device for the volume bar, this can be used to control the volume of the TV, but only for the built-in speakers of the TV |
| Update interval | Enter the update interval in seconds, this determines with which interval the plugin polls the TV (must be between 10 and 30 seconds) |
| Debug | When set to true the plugin shows additional information in the Domoticz log |

## Screenshots
![sony_tv](https://cloud.githubusercontent.com/assets/11230573/24884147/6fc63ec8-1e48-11e7-95aa-0020bcf6b666.png)

![sony_tv_vol](https://cloud.githubusercontent.com/assets/11230573/24884199/a0c53394-1e48-11e7-8d2f-2b4c0d417173.png)

![sony_tv_sources](https://cloud.githubusercontent.com/assets/11230573/24884202/a23478e8-1e48-11e7-85a4-51d0ef3a3e32.png)

![sony_tv_plugin_hardware](https://cloud.githubusercontent.com/assets/11230573/24884146/6fc5ce16-1e48-11e7-8d9a-ca7d4db8a7b8.png)

## Testing the plugin
To local test there is a `localtest.py` script that can be run from the command line.
Make sure you enter the IP address and PSK of your TV in `localtest.py`.
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

* KDL-42W805A --> with the use of cookies, check [this](http://www.domoticz.com/forum/viewtopic.php?f=65&t=16910&p=128866#p128866) for more information

* X8509C Android
