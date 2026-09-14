# Linux - Users

## Account types

In linux there are 4 types of accounts : 
- User Account : classic user
- Super User Account : root
- System accounts : ssh, mail
- Service Accounts : nginx, http

## Commands to check user informations

We can use the following commands : 
- `id` : list information about the current user
- `who` : list users currectly connected to the host
- `last` : list last users connected to the host

## Important User Files

Access control files : 
- `/etc/passwd` : give informations about users on the host
- `/etc/shadow` : store users password
- `/etc/group` : store information about all groups in the system

## Commands

We can disable account that are no use for the host : 

```bash
usermod -s /bin/nologin michael
```

The user would not be able to login to the host anymore.

To delete a user we can : 

```bash
userdel bob
```

To delete a group we can : 

```bash
groupdel devs
```

We can remove a user from group using : 

```bash
deluser michael admin
```

To update a password : 

```bash
passwd <username>
```

To create a user : 

```bash
useradd --uid=2328 --groups=admin --shell=/bin/bash --home-dir=/opt/sam sam
```

Create a user with a non interactive shell

```
useradd <name> -s /sbin/nologin
```

Create a user with an expiration date

```
adduser <name> -e 2024-12-24
```