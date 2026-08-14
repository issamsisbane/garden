[[Ansible Vault]]

# Installation

``` sh
python3 -m pip install --user ansible
```

We need to add the folder mentionned to path : 

``` sh
export PATH=$PATH:/home/issam/.local/bin
```

# Composants

## Inventory

On peut utiliser la commande suivante pour voir l'inventaire d'un certain hote, utile pour debugger la précedence des variables :

```bash
ansible-inventory -i inventory.ini --host my-host
```

## Playbook
`ansible-playbook -i inventory.ini playbook.yml --check`

Cette commande permet de faire un dry-run et de ne pas appliquer les changements mais seulement de voir ce qui aurait du se faire.

## Role

