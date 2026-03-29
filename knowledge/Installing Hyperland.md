Hyperland is a window manager.

# Graphical Applications

Basically there are two types of graphical application.

**Desktop Envrionment** : For example GNOME, a classic desktop environment

**Window Manager** : Simply a way of creating windows without a real complete graphical interface as we know

# Drawing screen

There is two protocol to draw a screen on linux.

**xorg**: 
	- 25 years old
	- non maintained

**wayland**:
	- new protrocol
	- problems with screen sharing and gaming

# Hyprland

https://wiki.hypr.land/Getting-Started/Master-Tutorial/
```
sudo pacman -s hyperland noto-fonts kitty
```

I followed the nvidia part but I remember I don't have a nvidia card on my laptop, I will have to clean this up.

 hyprland controls can be found in `.config/hypr/hyprland.conf`

```
###################
### KEYBINDINGS ###
###################

# See https://wiki.hyprland.org/Configuring/Keywords/
$mainMod = SUPER # Sets "Windows" key as main modifier

# Example binds, see https://wiki.hyprland.org/Configuring/Binds/ for more
bind = $mainMod, Q, exec, $terminal
bind = $mainMod, C, killactive,
bind = $mainMod, M, exit,
bind = $mainMod, E, exec, $fileManager
bind = $mainMod, V, togglefloating,
bind = $mainMod, R, exec, $menu
bind = $mainMod, P, pseudo, # dwindle
bind = $mainMod, J, togglesplit, # dwindle

# Move focus with mainMod + arrow keys
bind = $mainMod, left, movefocus, l
bind = $mainMod, right, movefocus, r
bind = $mainMod, up, movefocus, u
bind = $mainMod, down, movefocus, d

# Switch workspaces with mainMod + [0-9]
bind = $mainMod, 1, workspace, 1
bind = $mainMod, 2, workspace, 2
bind = $mainMod, 3, workspace, 3
bind = $mainMod, 4, workspace, 4
bind = $mainMod, 5, workspace, 5
bind = $mainMod, 6, workspace, 6
bind = $mainMod, 7, workspace, 7
bind = $mainMod, 8, workspace, 8
bind = $mainMod, 9, workspace, 9
bind = $mainMod, 0, workspace, 10

# Move active window to a workspace with mainMod + SHIFT + [0-9]
bind = $mainMod SHIFT, 1, movetoworkspace, 1
bind = $mainMod SHIFT, 2, movetoworkspace, 2
bind = $mainMod SHIFT, 3, movetoworkspace, 3
bind = $mainMod SHIFT, 4, movetoworkspace, 4
bind = $mainMod SHIFT, 5, movetoworkspace, 5
bind = $mainMod SHIFT, 6, movetoworkspace, 6
bind = $mainMod SHIFT, 7, movetoworkspace, 7
bind = $mainMod SHIFT, 8, movetoworkspace, 8
bind = $mainMod SHIFT, 9, movetoworkspace, 9
bind = $mainMod SHIFT, 0, movetoworkspace, 10
```

## Startup

https://wiki.hypr.land/Useful-Utilities/Systemd-start/

We need to use UWSM (Universal Wayland Session Manager) a wrapper around wayland for systemd.

```
pacman -S uwsm libnewt
```

In `~/.bash_profile` : 
```
if uwsm check may-start && uwsm select; then
	exec uwsm start default # hyperland.desktop to launch it directly
fi
```


what is a tty ?


# Housekeeping

our user doesn't have a home directory, so i created it manually. 

I had to do a localgen ot fix the connection error : 
```
warning setlocale LC_CTYPE cannot change locale
```
mount volume home to home directory (it wasn't created before so we didn't do it)

`/etc/fstab`

![[Pasted image 20250621165010.png]]

show bootloader menu before booting into arch linux

```
timeout 2          # 2 seconds before loading
default arch.conf  # boot file
console-mode max   # Max font size
editor no          # can't edit this file during the loading process
```

using `udev monitor` we can see what we plug in to our machine

# Security

https://wiki.archlinux.org/title/Security

## Firewall

https://wiki.archlinux.org/title/Security#Network_and_firewalls

We are going to use Uncomplicated firewall (ufw)
```
sudo -Syu ufw
```

We launch it : 
```
sudo systemctl enable ufw
sudo systemctl start ufw
```

First thing is to deny everything as a default rule : 
```
sudo ufw default deny
```

Allow traffic from home network : 
```
sudo ufw allow from 192.168.1.0/24
sudo ufw enable
```

## Arch Audit
```
sudo pacman -S arch-audit
arch-audit
```
![[Pasted image 20250622130642.png]]

## Pacman

To list all the files installed by a package
```
pacman -Ql minizip
```

## Lockscreen

https://wiki.hypr.land/Hypr-Ecosystem/hypridle/

We are going to use Hypridle & Hyprlock

##  NVIM


```
sudo pacman -S neovim wl-clipboard
```

we installing neovim there is a line saying we have to install wl-clipboard for wayland to handle paste.

## Dev Containers

https://wiki.archlinux.org/title/Docker

```
sudo pacman -S docker
sudo systemctl enable --now docker # enable and start the service
```

![[Pasted image 20250622152014.png]]

We need to add the user to docker group to use the socker.

```
sudo usermod -aG docker issam
```
We need to log out and in again to get the group change.

### DevPod

https://devpod.sh/docs/what-is-devpod

It's like devcontainers but non need for vscode (opensource).

https://devpod.sh/docs/getting-started/install
![[Pasted image 20250622160953.png]]

```
devpod ide use none # to use vim on the machine
devpod provider add docker
```

Il faut creer un fichier devcontainer.json comme on le ferait avec vscode. 

We launch with : 
```
devpod up .
```

We ssh to it using : 

```
ssh name.devpod
```

I had an error saying [::1]:53: read connection refused. It can be solved by using this command :  
https://wiki.archlinux.org/title/Systemd-resolved
```
sudo ln -sf ../run/systemd/resolve/stub-resolv.conf /etc/resolv.conf
```