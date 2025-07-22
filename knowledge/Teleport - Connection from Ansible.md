Pour connecter ansible à Teleport il faut suivre les étapes suivantes : 

We need to follow this tutorial : 
https://goteleport.com/docs/enroll-resources/server-access/guides/ansible/

Il faut au préalable se connecter via tsh login.

Créer un ssh.cfg file : 
``` sh
tsh config > ssh.cfg
```

Créer le ansible.cfg :
``` yaml
[defaults]
host_key_checking = True
inventory=./hosts
remote_tmp=/tmp

[ssh_connection]
scp_if_ssh = True
ssh_args = -F ./ssh.cfg
```

Créer le hosts file : 
``` sh
tsh ls --format=json | jq '.[].spec.hostname + ".eks.snzs.live"' > hosts
```

Ajouter le nom de group des hosts : 
```
[all]
myip
myip2
```

Creer un playbook bidon : 
``` yaml
- hosts: all
  remote_user: ubuntu
  tasks:
    - name: "hostname"
      command: "hostname"
```

Dans le repo git tout sera déjà ajouté. Il faudra seulement lancer le script init-teleport.sh avant d'utiliser ansible pour faire les configs nécessaires pour la connexion.

``` bash
#!/bin/bash

# Check Teleport Login Status
echo "Checking Teleport login status..."
if ! tsh status &>/dev/null; then
  echo "You are not logged in to Teleport. Please log in first using 'tsh login' and then re-run this script."
  exit 1
fi

# Generating file ssh.cfg with Teleport
echo "Generating ssh.cfg file with Teleport"
tsh config > ssh.cfg
```

# Playbook Teleport Agent
1. Ajouter IP de la machine Teleport dans le fichier hosts de la machine
2. Générer un token via `tctl nodes add -ttl 1h`
3. Executer dans la machine le script avec le token