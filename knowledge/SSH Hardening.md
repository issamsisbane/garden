# SSH Hardening

Disable root login and password authent : `/etc/ssh/sshd_config`

```
PermitRootLogin no
PasswordAuthentication no
```

```bash
systemctl restart sshd
```