We want to install [[K3S]] on out raspberry pi.

# Requirements

There are some requirements to do first.

## Make sure the system is up to date

``` bash
sudo apt update
sudo apt upgrade
```

## Install VIM

We need to adjust cmdline.txt which is a list of command ran at the raspberry boots.

## Enable Cgroup

K3S install [[Containerd]] under the hood to be able to launch container. So we need to enable [[Cgroup]].

``` bash
sudo vim /boot/firmware/cmdline.txt

# We add this on the same line
cgroup_memory=1 cgroup_enable=memory

# Reboot the raspberry
sudo reboot
```

## Install K3S
```
sudo su -
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--disable=helm-controller" sh
systemctl status k3s
```

We do not want to install the helm controller because we will install Flux later that use its own helm controller. 

K3S install kubectl and configure it to allow us to interact with the cluster from the raspberry.

## Access the cluster from outside

We don't want to ssh to the raspberry everytime. 
So we need to configure kubectl to access the cluster in our pc.

The kubeconfig file is here : 
`/etc/rancher/k3s/k3s.yaml`

``` bash
# Copy to home directory
cp /etc/rancher/k3s/k3s.yaml .

# Make sure we have the rights to copy it through ssh
chown issam:issam k3s.yaml
```

We need to copy the file to the host : 
``` bash
scp issam@raspberrypi:/home/issam/k3s.yaml .
```

Then we need to add it to `.kube/config`.
We also need to replace the ip in the config file from `127.0.0.1` to the api of the raspberry pi.