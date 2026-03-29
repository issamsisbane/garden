I followed the following page : https://wiki.archlinux.org/title/Installation_guide

# Launch the arch linux installation

I had to do this again using rufus : [[Install Linux]]
I also has to disable secure boot.

# Configuration

If we shutdown the machine before the end of configuration we have to redo everything.

I get this page : 

![[Pasted image 20250617225816.png]]

## Connect to Internet

We use the tool [[iwctl]] preinstalled to connect to our WIFI network : 
![[Pasted image 20250617231459.png]]
![[Pasted image 20250617231515.png]]

We can see our IP address and we can try a curl to verify : 
![[Pasted image 20250617231520.png]]

## Setup ssh

Next step is to setup SSH in order to do the configuration from our PC.

1. Verify that sshd is running (It should be already installed)
2. Set a password for the current user
![[Pasted image 20250617231527.png]]
3. We can connect from our PC via : 
`ssh root@archiso` and using the password we just set.

## Update system clock

`timedatectl`

## Partition the disks

See the current partitions : 
```
lsblk
```

![[Pasted image 20250618223958.png]]
- `loop0` unstalled by arch linux installation
- `sda` : hdd separated in 2 => maybe the installation of Linux Mint did that sda1 for the EFI partition used by the operating system for UEFI and sda2 the root / partition of Linux Mint
![[Pasted image 20250618231548.png]]
- `sdb` : usb key with the arch linux ISO

Everything in linux is files. 

If we go to `/dev` we can see all the devices that are on the system
![[Pasted image 20250618224557.png]]

we can point to on partition with /dev/sda1 for example.

### How to partition
[[Linux - Partitionning]]

We will use the new way with LVM.
We would have 1 boot partition and the rest would be a big partitions where we will create logical volumes for  various purpose of different sizes. It would then be easy to resize delete and create.

A logical volume can span across several storage devices

### Why encrypt ?
When using an operating system we *MUST* encrypt it, if we don't if someone stole our physical computer he would be able to read what is inside our HDD or SSD because it's not encrypted with a key that only us have (unless we get unintelligible data)

![[Pasted image 20250618230559.png]]

I had linux mint installed previously on the machine so I already have a paritionned sda disk on my sda device (hdd). I had nothing important in there. 

To delete we do : 
![[Pasted image 20250618231631.png]]

We can start again from a clean drive.

### Partionning

We will use fdisk.

We can see the command we can use using m : 

![[Pasted image 20250618232415.png]]

![[Pasted image 20250618232413.png]]

First thing to do is to create a new [[Linux - GPT Partition Table]]. It's the table saying where the partitions are... It's keeping trace of all partition on the disk using unique identifiers.

Then we follow what is advised in [here](https://wiki.archlinux.org/title/Installation_guide) : 
![[Pasted image 20250618232712.png]]


First partition : 
![[Pasted image 20250618232500.png]]

We have to change the type to EFI System : 
![[Pasted image 20250618232612.png]]

Second Partition that will take all remaining spaces :
![[Pasted image 20250618233053.png]]
The second partition start at the end of the first until the last remaing sector.

We have to change the type to Linux LVM (if we quit without writing all changes are lost) : 
![[Pasted image 20250618233210.png]]

Finally we have : 
![[Pasted image 20250618233447.png]]

We have to write to apply the changes :
![[Pasted image 20250618233600.png]]

## Encryption

We will use [[dm-crypt]].
We can follow this https://wiki.archlinux.org/title/Dm-crypt/Encrypting_an_entire_system#LVM_on_LUKS

We will use [[LUKS]]

![[Pasted image 20250618234457.png]]

We can do this to be really secure : 
![[Pasted image 20250618234628.png]]

But we will just use a passphrase.

Before starting we should preparing the disk by performing a secure erase by overwriting the entire device with random data. But we don't really care about the old data of this laptop.

`sda1` : boot partition
`sda2` :  encrypted container

We do this to setup the encrypted container : 
![[Pasted image 20250618235513.png]]

Open the container : 
![[Pasted image 20250618235702.png]]

We will now create the physical volume :
![[Pasted image 20250619000637.png]]

We create the volume group : 
![[Pasted image 20250619000811.png]]

We create the logical volumes : 
![[Pasted image 20250619000829.png]]

The [[Swap]] is 1x the ram if I have 8gb RAM for example but its depends on the size of the RAM.

![[Pasted image 20250619000913.png]]

[[File System Format]]
We then need to format our partitions with a particular filesystems format to allow the operating system to know what is on there and how to handle files. It can also optimize performance for certain tasks depending on the fs format.

![[Pasted image 20250619001607.png]]

What we have now : 
![[Pasted image 20250619001650.png]]

Volumes on disk are only accessible until you mount the block devices.

Format and mount the UEFI boot partitions : 
![[Pasted image 20250619002402.png]]

When we update the size of a partition we have to update the fs size using (even if it's mounted for increasing size but have to unmount to decrease ) : 

```
resize2fs /dev/pv/volume # For ext fs format
```

We return to the installing guide.

We mount the root volume : 
![[Pasted image 20250619003406.png]]

We have to mount the /mnt before the /mnt/boot.

We enable the swap volume : 
![[Pasted image 20250619003800.png]]

# Installation

We install the base package of linux kernel :
 ![[Pasted image 20250619004049.png]]
This is the actual installation of arch linux

It created a fully functionnal OS in /mnt

FSTAB

the fstab file automatically mount partition when the system is started.
![[Pasted image 20250619005628.png]]
we can see our parition which are going to be mounted at the start of the system.

CHROOT

we need to change root to the new system we installed in /mnt. It's like we boot in this new system.
Until now we where using the usb key with the temporary fs to install arch. Now we are and the arch system we install on our hdd. We are using this new os as the current context.

TIME

![[Pasted image 20250619010140.png]]
![[Pasted image 20250619010149.png]]

We created a symbolic link to our localtime.
We then sync the clock : 

![[Pasted image 20250619010310.png]]

INSTALLING PACAKGES NEEDED 
![[Pasted image 20250619011102.png]]

We also install which, sudo and man commands.
![[Pasted image 20250619010917.png]]
![[Pasted image 20250619010909.png]]

for now we just want a minimal os that we can boot on :
- which
- man
- sudo
- intel-ucode (because intelcpu)

SYSTEMD

all process start from systemd a modrn init process : 
![[Pasted image 20250619011650.png]]

When you load a pc it's the BIOS does its  POST (Power on self test check is the hardware is working correctly), then will be looking for the /boot partition.
On this partition there should be a boot loader (GRUB a standard boot loader for linux)=> loads an OS => start with the init process.

old init process sysV init
new systemd => violate the UNIX philosphy because it''s not doing only one thing and well but many things.

Now every modern Linux systems use systemd as init process.

To Interact with systemd we us `systemctl`.
Systemd works with unit files for systemd UNITS meaning anything managed by systemd.

enabling a service means it will load at the boot of the OS.

systemd services conf : 
![[Pasted image 20250619013254.png]]

NETWORKING

We need to configure networking by activating services to allow the devices to connect to internet at startup. why ???

network manager vs systemd & networkd

https://wiki.archlinux.org/title/Systemd-networkd

Networkd

![[Pasted image 20250619012557.png]]

we need to start/enable systemd-networkd : 
![[Pasted image 20250619012900.png]]
we can't start it yet because we are in chroot but it will be launch at startup.

networkd will configure the network interfaces...

Resolved

we need systemd-resolved responsible for dns resolving.

Systemd network files

![[Pasted image 20250619013331.png]]

enp1s0 => cable
wlan => wifi

we create the file `/etc/systemd/network/25-wireless.network` : 

```conf
[Match]
Name=wlan0

[Link]
RequiredForOnline=routable # the system will be online only if can go outside the local network

[Network]
DHCP=yes
IgnoreCarrierLoss=3s
```

the 25 is for the order of conf file.

IWD

then we need to install iwd :
![[Pasted image 20250619014058.png]]

and enable it : 
![[Pasted image 20250619014140.png]]

we notice that we are already sudo on the machine.

LOCALIZATION

lcoales are used to render text monertary value...

we need to edit text but we dont have an editor yet. We have to install one : 

![[Pasted image 20250619010652.png]]

we need to decomment `LANG=_en_US.UTF-8` in /etc/locale.gen
and create the file /etc/locale.conf with the contenet `LANG=_en_US.UTF-8`

- Syu update all packages and mirror

INITRAMFS
we return to the encrypt page
https://wiki.archlinux.org/title/Dm-crypt/Encrypting_an_entire_system#LVM_on_LUKS
4.4

it's a scheme for loading a temporary root file system into memory to be use as the part of the linux startup process.

We are using cryptology so at boot the system will need to decrypt the disk to allow us to access the os.

We need to add hooks to the file mkinitscpio.conf. mikinitscpio create a initial ramdisk environment whit the capabilities we give it.

![[Pasted image 20250619015436.png]]

```
HOOKS=(base **systemd** autodetect microcode modconf kms **keyboard** **sd-vconsole** block **sd-encrypt** **lvm2** filesystems fsck)
```

we have error we need to do some things :
![[Pasted image 20250619020043.png]]

we can add bigger font of the terminal that starts before the system decryption (very small unless) : 
/etc/vconsole.conf : `FONT=latarcyrheb-sun32`

wecan check if it exists : 
![[Pasted image 20250619020332.png]]

then we install the lvm2 package : 
`pacman -Syu lvm2`

relaunch : `mkinitcpio -P`

# Boot Loader

https://wiki.archlinux.org/title/Arch_boot_process#Boot_loader
what is the differences between bootloaders ?

GRUB is a standard bootloader for linux.
Systemd has its own bootloader : systemd-boot

https://wiki.archlinux.org/title/Systemd-boot

It's already in the base package.

![[Pasted image 20250619021705.png]]

what is ESP ?

install it : 
![[Pasted image 20250619021737.png]]
warning because chroot.

We have this now : 
![[Pasted image 20250619021959.png]]

in the entries directiry we will have the different files stating options to boot (windows, linux...)
`arch.conf`
![[Pasted image 20250619022407.png]]


![[Pasted image 20250619022532.png]]

we will use 

![[Pasted image 20250619022709.png]]

because we are using systemd

```
title # title displayed
linux # the file to load
inird # manifest generated by mkinitcpio conf

options rd.luks.name=device-UUID_=cryptlvm root=/dev/MyVolGroup/root 
# allow to init the decryption process at boot
# the partition needed to be decrypted and the logical volume needed to mounted as fs
``` 
The device UUID is the UUID of the actual partition.

inserting the content of the command blkid : 
![[Pasted image 20250619023155.png]]
finally its : 
![[Pasted image 20250619023438.png]]

# Create a user

```
useradd issam
usermod -aG wheel issam
passwd
passwd issam
```

uncomment in visudo to allow wheel users as admin (need the sudo package)

```
visudo
```
![[Pasted image 20250619024105.png]]

# Reboot

unplug the usb key
set the hdd to first in the bios (F2)
do again the step to connect to wifi