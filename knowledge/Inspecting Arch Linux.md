# SSH

Install Fundamentals : 
```
sudo pacman -Syu openssh
sudo pacman -Syu bash-completion
```

I tried to ssh into the machine from my PC but I couldn't. In found that I had only an ipv6 address and not ipv4 for my interface. Finally it was juste in the file /etc/systemd/network/25-wireless.network : 

```
[Match]
Name=wlan0 # and not wlan

[Network]
DHCP=yes
IgnoreCarrierLoss=3s
```

The name should match the exact name of the interface we want to use (here wifi so wlan).

I can now ssh to my machine.

# Processes

We can see all the unique processes running using : 
```
pstree
```
![[Pasted image 20250621144834.png]]

## Dbus-brocker
The first one is dbus-brocker, it's a way for processes to communicate through each other based on a message system. It's the `server` receiving and transferring messages.

## IWD

This is the Wireless service allowing iwctl command to configure the wifi connection.

## Login

To log to the machine

# Services

## SSHD

to use ssh

## SD-PAM

System libraries that handles the authentication tasks of application (services) on the system. 

## Journal

This is for logging

## Logind

handles everything that has to log.

## Network

## Resolve

## UDEVD

handles everything about device event, premissons of devices...

## USERDBD

A unified interface to work with user and groups

# RAM

We can check ram usage using :
```
free -d
```
We can see that we have the swap memory.

The system only uses 375 Mi of RAM...
![[Pasted image 20250621150459.png]]

We can use htop to monitor the cpu usage : 
```
sudo pacman -Syu htop
```
![[Pasted image 20250621150637.png]]