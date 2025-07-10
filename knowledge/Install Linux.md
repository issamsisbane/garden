# 1 - Download linux

Download a linux distribution iso such as [Linux Mint](https://linuxmint.com/) or [Ubuntu](https://www.ubuntu-fr.org/).

# 2 -  Create a Bootable USB Key

We need an usb key, 8gb minimum.
We need to install rufus an launch it :
![[rufus_screenshot.png]]

We select our USB key and we select the iso we download and then we just it `Start`.

# 3 - BIOS Boot Settings

Next, we plug our USB key to the laptop or the PC we want to install linux and we need to enter the bios. 
You have to power on your pc and press a specific key depending on your motherboard or laptop manufacturer. 

Once you into the bios, you have to change the boot order and put the usb key at the the top.
Then save and your pc must restart with a command line asking to launch ubuntu, press enter and just follow the steps to install linux (or click install linux in the desktop if nothing happens).
# Troubleshooting
Reset system error when installing linux on an acer laptop. Resolved using this : 
https://itsfoss.com/no-bootable-device-found-ubuntu/

i also changed the boot order and setting the one created as top 1.