Set up password-less ssh access to root user in remote machine.
1. Generate a ssh-key
```sh
ssh-keygen
```
2. Copy the public keys to all machines
```sh
ssh-copy-id user@host
```