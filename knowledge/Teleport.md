![[Pasted image 20241027152717.png]]

# Setup Teleport

Installation setup
https://goteleport.com/docs/admin-guides/deploy-a-cluster/linux-demo/

## Installation on Bastion

We need to install teleport and all the tools : 
``` sh
curl https://cdn.teleport.dev/install-v16.4.6.sh | bash -s 16.4.6
```

## Configure teleport

If we have a hostname and we want automatic tls : 

``` sh
sudo teleport configure -o file \
    --acme --acme-email=issamsnz@proton.me \
    --cluster-name=eks.snzs.live # hostname of the bastion for certificate
```

If we already have a certificate :
``` sh
sudo teleport configure -o file \
    --cluster-name=eks.snzs.live \
    --public-addr=eks.snzs.live:443 \
    --cert-file=/var/lib/teleport/fullchain.pem \
    --key-file=/var/lib/teleport/privkey.pem
```






## Launch Teleport

> [!IMPORTANT] Process
> In production we would want to create a processus to launch it : 
> 
> ``` sh
> sudo systemctl enable teleport
> sudo systemctl start teleport
> ```

Just for testing we would use this command to launch it one time : 

``` sh
sudo teleport start --config="/etc/teleport.yaml"
```

Then we should be able to access the teleport web portal using the hostname we provide earlier `https://eks.snzs.live`

## Creating an admin user

To connect to the teleport portal, we need to create a user. 

``` sh
sudo tctl users add teleport-admin --roles=editor,access --logins=root,ubuntu,ec2-user
```

It should prompt and url to set up password and OTP : 

``` 
User "teleport-admin" has been created but requires a password. Share this URL with the user to complete user setup, link is valid for 1h:
https://teleport.example.com:443/web/invite/123abc456def789ghi123abc456def78

NOTE: Make sure teleport.example.com:443 points at a Teleport proxy which users can access.
```

My credentials are : 
```
user : teleport-admin
pass: myteleportpassword
```

then we can access the portal. 

## Add a machine to teleport

![[Pasted image 20241027175112.png]]

![[Pasted image 20241027175016.png]]

We just need to select the machine type. 

Then we have to copy paste this line of code to our machine and it should be added to teleport.

![[Pasted image 20241027175131.png]]

# Connect to machine

To connect to our machine we need the tsh command line tools.
It could be install following this tutorial. 
https://goteleport.com/docs/connect-your-client/tsh/

Then we need to : 
``` sh
tsh login --proxy=eks.snzs.live --user=teleport-admin
```

To connect to a machine we just need to copy the hostname of the machine and : 
``` sh
tsh ssh ec2-user@ip-10-0-2-57.eu-west-3.compute.internal
```

# ANSIBLE + TELEPORT

We need to follow this tutorial : 
https://goteleport.com/docs/enroll-resources/server-access/guides/ansible/

We need to create an ssh.cfg file : 
```
tsh config > ssh.cfg
```

Create an ansible.cfg file :
```
[defaults]
host_key_checking = True
inventory=./hosts
remote_tmp=/tmp

[ssh_connection]
scp_if_ssh = True
ssh_args = -F ./ssh.cfg
```

Create the hosts file : 
```
tsh ls --format=json | jq '.[].spec.hostname + ".eks.snzs.live"' > hosts
```

```
[all]
myip
myip2
```

Create a playbook : 
```
- hosts: all
  remote_user: ubuntu
  tasks:
    - name: "hostname"
      command: "hostname"
```

And then launch the playbook : 
```
ANSIBLE_CONFIG=./ansible.cfg ansible-playbook test-playbook.yml
```

I add to specifify the config file because it wasn't recognize by ansible without.