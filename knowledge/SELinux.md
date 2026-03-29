Sur CentOS on installe SELInux de la façon suivante et on reboot la machine : 

```
yum install selinux-policy-targeted
yum install selinux-policy-devel policycoreutils
touch /.autorelabel; reboot
```

Pour desactiver SELinux, on fait : 

```
sudo setenforce 0
```