/etc/ssh/sshd_config
```
PermitRootLogin: no
```

Il faut recharger le serbvice ssh apres.

```
sudo systemctl restart sshd
```