# Seccomp

Currently there are 435 syscalls in linux and all of them can be used by default by application running in the user space to carry out hardware and networking tasks.

In reality no applications need to make this many syscalls. So not restricting syscalls increase the attack surface.

Seccomp (Secure Computing) is a linux kernel feature that can be use to sandbox applications to only use syscalls they need.

In order to know  if kernel in the host support seccomp, we need to check the boot config file : 

```bash
grep -i seccomp /boot/config-$(uname -r)
```

If we have `CONFIG_SECCOMP=y` its ok.

**Malicious Use Exemple** : "The CVE-2016-5195 (DIRTY COW Exploit) describe a situation when it is possible to write on a read-only file and making out of the container using the ptrace() syscall.

We can see the status of seccomp got a process using : 

```bash
grep Seccomp /proc/<pid>/status
```

Secomp as 3 modes : 
- Mode 1 : DISABLED
- Mode 2 : STRICT only 4 syscalls are allowed (read, write,exit and sigreturn)
- Mode 3 : FILTERED selectively filter syscalls using by default by docker.

Docker has a builtin seccomp filter that is used by default when creating a container if the host as seccomp enabled.

This feature is available only if Docker has been built with `seccomp` and the kernel is configured with `CONFIG_SECCOMP` enabled. To check if your kernel supports `seccomp`:

```bash
grep CONFIG_SECCOMP= /boot/config-$(uname -r)
CONFIG_SECCOMP=y
```

This is an exemple of this file, it restrict 60 of 435 linux syscalls (including the ptrace()). Only around 375 are available.

There are 2 modes : 

![[Kubernetes_-_CKS_29.png]]

- Whitelist mode : We need to explicitly list all allowed syscalls, if not listed the syscall will fail with an error
- Blacklist mode : By default all syscalls are allowed but those listed on the list
  
Whitelist is very restrictive and Blacklist can be too open.

By default docker is in whitelist mode : https://github.com/moby/profiles/blob/main/seccomp/default.json

https://docs.docker.com/engine/security/seccomp/

Syscalls blocked by default are : 
- clock-adjtime
- clock-settime
- reboot
- mount
- umount
- settimeofday
- create_module
- swapoff
- stime
- delete_module
- ...

The default seccomp conf file for docker is quite open, so we can make use of a custom seccomp file more restrictive.

For exemple, we can restrict the creation of directory like this : 

![[Kubernetes_-_CKS_30.png]]

We need to tell docker to use a particular json seccomp file for our container.

We can also disable the use of seccomp by using this :

```bash
docker run -it --rm --security-opt seccomp=unconfined docker/whalesay /bin/sh
```

> [!Warning] IT IS A VERY BAD IDEA TO DO THIS AS ALL SYSTEMCALL WILL BE AVAILABLE IN THE CONTAINER.

As a note, if we attempted to change date in an unconfined docker container it will failed due to other security restriction used by docker.

We can run a container to learn more about the blocked syscalls :

![[Kubernetes_-_CKS_31.png]]